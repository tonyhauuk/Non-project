/*
漫抓采集程序，根据网站列表采集网站信息
代码越少越好
这个版本。
 1、同一时间只能一个网站只能被一个线程采集，lock很重要，或者web的num_wget
 2、各个线程各自为政,自己定义采集圈数，同一个时间只能拥有一个多层采集的网址
 3、网址的采集圈数是实际被采集的圈数
 4、引入一个采集圈数因子loopfast,叫最快采集圈数
 5、网址是否锁定用num_nodelink_working
 6、loop
	loop_WQ 是队列的圈数，现在只有统计意义
	loop_web是网站的圈数 ，0表示未采集过，1以上表示采集次数，用这个指标界定网址的儿子链接是否认为是新链接，对那些数字报纸的网站很有用，一般滚动频道的新文章是否做深度采集，用分析库合作实现
	loop_thread是线程工作的圈数，他变化很大，一旦搜索到网址队列尾部就升级了，不能拿他做很多判断
	loop_link是链接的圈数，第一次采集默认0，采集之后设置为1，每采集一次加1
	loop_link_database 是链接在数据库中存储的圈数

15的版本可能会在同一时间重复采集
gcc -o estar_manzhua_mysql estar_manzhua_mysql.c -lpthread estar.c hash.c xmalloc.c -lssl -L/usr/lib/mysql -lmysqlclient -lm
20150525
自由扫描式，没个线程自由扫描


mysql -uweb_dev -pwebdevwebdev -h124.237.121.25
mysql -uroot -pestar2005mysql
use news_dup

select count(*) from E_dup_link;
TRUNCATE TABLE `E_dup_link3`

20180704 继承227
1、这版主要改动，利用动态IP的VPS采集搜索引擎
2、config.cfg 增加了connect连接互联网方式
3、关键词队列，拆分，按余数
4、long %u
5、size_t 的几个函数
6、增加采集数量统计，传送web服务器

20180726
这个版本和17完全不通，是继承manzhua26过来的。
1、Connection修改为配置文件种字符串表示
2、编译中，32位独立mygo.sh，去重64位编译多余参数。
3、下载配置文件，增加端口设置功能（有些服务器禁止使用22端口）

20180727
完全继承28版
20180728
1、修改strtoul修改为atoi(row[0]); 避免64位long问题

20180729
1、增加了downloadtools 选项，wget,chrome,phantomjs
2、修改了total.txt 写文件增加全路径，否则会写到采集文件目录下。
3、修改了weixin.py，取消了chrome，4小时清理一次的机制

20180730
1、释放mysql_free_result屏蔽

20180731
1、增加了ConnDatabase()为了解决64数据库出现MySQL server has gone away问题

20180804
1、mysql_free_result 不释放这个，可能在64位系统中有问题，现在恢复释放

20180805
1、mysql_free_result 必须与mysql_store_result()， mysql_use_result()， mysql_list_dbs()，成对使用，所以还是清除了mysql_free_result    https://dev.mysql.com/doc/refman/5.5/en/mysql-free-result.html

20180808
1、修改readweb，引起网址列表只有一个时中断，http://toutiao.com/       2       1152856        toutiao

20180810
1、取消TotalQLWebQueue()
2、readweb_by_kw（）修改了，如果关键词长度为0，则continue
3、add_nodelink_to_sh（）增加了对微信的约束，在sh的小队列中，只能有一个微信搜索任务。
4、nodeWQ->num_web_working 新参数，定义一个采集队列，正在工作的web数量，这个参数可以约定微信或其他队列，通一时间可以采集几个网址，微信搜索收到限制，但微信信息不限制，这样可以区别对待，提高采集效率,这个改动比较大，注意。
     find_a_nodeWeb()函数做了微信约定

 20180812
 1、修改clear_link()一个错误，连接中双‘//’问题
 2、增加 Connection_server
 3、正式转移30版------------------------------------------------------------------------

 20180813
 1、修改了fclose_run_a_sh（）的下载工具选项
 2、修改get_working_wget_baseinfo()增加文件名尾部下载工具，供server方式寻找自己的任务文件

 20180814
 1、支持在confg.cfg设置2个微信采集队列，见97服务器，注意把小队列放前边，这样可以不被大队列去重掉。
 2、再修改为队列决定采集方式

 20180910
 1、支持微信单个sh增加web任务，其他sh处理首页解析的连接。提高采集效率
 2、config的tools设置
 3、增加了WebServerWeb采集方式，即自己设置微web服务器，wget调用这个微服务采集微信、今日头条等防采集的网站。
 4、QLShield_FileType_Check（）函数修改bug,非常严重的bug
 4、很多改进

 20180912
 1、未来改进：
 	a、修改wget为libcurl 方式
 	b、修改为c++
 	c、更多利用第三方库，比如libxml2      参考https://curl.haxx.se/libcurl/c/example.html
 	d、电子版报纸采集
 	e、微博信息采集
 	f、修改目录任务模式，利用flask和wget建立采集微服务模式，带宽利用率更高

 20180920
 1、增加merge_url_dir()函数，并且优化了，链接合成，这是重大修改

  20180925
 1、修改了sina的微博提取模板
 2、修改了sina的微博链接
 3、新浪微博改版后，已经可以识别代理服务器背后的ip,目前，
 	a、如果原机时国外的可以使用代理服务器采集，如果原机时国内的不能使用代理服务器采集，只能浏览器采集(谷歌等)。
 	b、有意思，杭州电信VPS用代理服务器方式无法采集微信，但联通线路可以，而且挺快。2台机器可以组网，如果用webserver方式采集至少要用4台，和微信一样，最好用联通线路。
 	c、wget+代理服务器，方式采集占用服务器资源小，chrome +webserver，占用服务器资源大
 	d、联通线路采集微信好像不稳定
*/
//char Encadir[100]="/dev/shm/enca/";

#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <sys/time.h>
#include <sys/stat.h>
#include <unistd.h>
#include <fcntl.h>
#include <dirent.h>

//原来时调用下边2行，后修改为function/estar.h，如果发现有问题，再置换。20180622
//#include "./estar.h"
//#include "./hash.h"
#include "../function/estar.h"


#include "./shield.h"

#include <string.h>

#include <mysql/mysql.h>
#include <openssl/md5.h>

#include <unistd.h>
#include <netdb.h>
#include <arpa/inet.h>
#include <stdlib.h>
#include <sys/ioctl.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <net/if.h>
#include <C_CkHttp.h>

#define NotUseProxy  -1

int  	MyDebug  ; //调试模式
int  	IfDownload ; //是否下载网址库等信息
int  	MaxWebSize = 2048000;//最大网页大小，http://nb.house.sina.com.cn/scan/居然1.3M  1373992
char 	NowWorkingDir[200];

int 	BigLoop;
int 	LimitRate;// = 30000;//30M
int 	onewgetLimitRate;// = 50;//50k
int 	IfCheckCenter=0;//是否进行链接汇总查询
char 	CheckCenterLink[200];//汇总查询链接
//int		PPPOE;//pppoe 拨号，0本服务器无拨号功能，1本服务器有拨号功能

//下载信息
#define  Download_BadForever 	-110 //永久坏链接
#define  Download_TooBig 		-105 //太大 采集1次
#define  Download_TooSmall  	-3 //太小 采集2次
#define  Download_Timeout  		-2 //超时 采集2次

#define  Download_Line  		0 //下载分界线

#define  Download_Undetermined  	1 //待定
#define  Download_OKInit  			2 //链接下载初始化OK
#define  Download_OKTrue  			3 //自己下载成功的
#define  Download_OKForever  		5 //链接下载永久OK

struct MYNUM{
		int  thread_all;
		int  thread_web;//网页下载数量
		int  thread_weibo;//主微博采集线程数量
		int  thread_weixin;//微信采集线程数量
	 	int  thread_search;//采集搜索引擎的线程数量
	 	int  thread_weibo_search;//微博搜索的数量
	 	int  thread_download_index;

		int  FirstWork;
		int  goodproxy;//队列使用代理的数量
		int  proxy;//总计代理服务器下载数量
		int  WebQueue; //采集队列的数量
		//int  QLWebAll_proxy;//需要代理服务器的数量

		int wget;//同时工作的wget 个数
} Num;





struct QNodeLink;

struct QNodeShieldWeb;
struct QListShieldWeb;
struct QListShieldWeb	*QLShieldWeb;//屏蔽网址队列
//struct QNodeShieldWeb 	*InsertQLShieldDomain(QListShieldWeb* QL, char * domain  );
/*
char FileKwDeleteHtml[500]="kw_delete_html";
char **KwDeleteHtml; //网页关键词
int Num_KwDeleteHtml=0;
*/
//tinytype
//web
#define IsNormal 0
#define IsReplaceWeb 1
#define IsError 2
//weibo
#define IsSina 10
#define IsQQ 11
#define Iszhongsou 12
#define Isbaidu 13

#define IsInfo 1
#define Ischannel 0

/*
//Proxy
#define  Proxy_no 	0	//不使用代理服务器
#define  Proxy_web 	1	//仅web使用，就是第0层
#define  Proxy_all 	2	//所有连接都使用
*/




//链接方式
#define  Connection_direct  		0 //直连

#define  Connection_proxy_web		1 //代理服务器 只有0层用，就是网页用，二级以上连接不用
#define  Connection_proxy_all		2 //都用

#define  Connection_pppoe_web		3//动态vps 拨号 0层用
#define  Connection_pppoe_all		4//动态vps 拨号 1都用

const char *ConnectionStr[]={"direct ","proxy_web","proxy_all ","pppoe_web","pppoe_all"};



//Tools 读取文件下载工具，实际上是指定web下载方式
#define	ToolsWget 				0	//使用wget命令行方式

#define	ToolsPhantomjsWeb 		1	//使用phantomjs的js程序采集行方式
#define	ToolsPhantomjsAll 		2

#define	ToolsChromePythonWeb		3//使用chrome的python程序采集,需要启动浏览器，速度慢
#define	ToolsChromePythonAll		4

#define	ToolsChromeCommandWeb 		5	//使用chrome命令行方式采集
#define	ToolsChromeCommandAll 		6

#define	ToolsDirServerWeb 			7	//使用后台server，是目录方式
#define	ToolsDirServerAll 			8

#define	ToolsWebServerWeb 		9	//使用后外webserver,是web方式
#define	ToolsWebServerAll 		10


const char *ToolsStr[]={"wget","PhantomjsWeb","PhantomjsAll ","ChromePythonWeb","ChromePythonAll","ChromeCommandWeb","ChromeCommandAll","DirServerWeb","DirServerAll","WebServerWeb","WebServerAll"};


/**********************************************************************
//锁定下载工具类
***********************************************************************/
struct DownloadTools{
	char url[100];
	int tools;
}**DownloadToolsArr=NULL;

int DownloadToolsArrNum = 0;

/**********************************************************************
//锁定下载工具
***********************************************************************/
/*
int DownloadTools_Get(char *url , int  nodeWQ_tools , int web_or_link){

	if( 	ToolsDirServerAll == nodeWQ_tools || ToolsDirServerWeb == nodeWQ_tools && IsWeb==web_or_link)
		return ToolsServerWeb;
	else if(  ToolsWebServerAll == nodeWQ_tools || ToolsWebServerWeb == nodeWQ_tools && IsWeb==web_or_link)
		return ToolsWebServerWeb;
	else if(         ToolsPhantomjsAll == nodeWQ_tools || ToolsPhantomjsWeb == nodeWQ_tools &&  IsWeb==web_or_link )
		return ToolsPhantomjsWeb;
	else if(	 ToolsChromePythonAll == nodeWQ_tools ||ToolsChromePythonWeb == nodeWQ_tools &&  IsWeb==web_or_link )
		return ToolsChromePythonWeb;
	else if(  ToolsChromeCommandAll == nodeWQ_tools ||ToolsChromeCommandWeb == nodeWQ_tools &&  IsWeb==web_or_link )
		return ToolsChromeCommandWeb;
	else
		return ToolsServerWeb;


	//暂时废弃掉特殊连接指定采集工具的功能
	struct DownloadTools *downloadtools;
	int i;
	for(i = 0 ;i <DownloadToolsArrNum ;i++){
		downloadtools = DownloadToolsArr[i];
		if(strstr(url , downloadtools->url )){
			return downloadtools->tools;
		}
	}

	return ToolsWget;
}
*/
/**********************************************************************
//读取文件下载工具
#define UseWget 			0	//使用wget命令行方式
#define UsePhantomjs 		1	//使用phantomjs的js程序采集行方式
#define UseChromePython		2	//使用chrome的python程序采集
#define UseChromeCommand 	3	//使用chrome命令行方式采集
#define UseServer 			4	//使用后台server
const char *ToolsStr[]={"wget","phantomjs","chromePython","chromeCommand","server"};

***********************************************************************/
/*
void DownloadTools_Read(){
	DownloadToolsArrNum = 0;
	DownloadToolsArr = NULL;
	struct DownloadTools *p ;
	char filepath[500];
	sprintf(filepath , "%s/download_tools_url.txt",NowWorkingDir);
	char url[500],type[50];
	FILE   *FILE_web_linkfile;
	FILE_web_linkfile=fopen(filepath,"r");
	if (FILE_web_linkfile == NULL) {   printf("DownloadToolsRead can not open the file-----file=%s\n",filepath); }
	else{
		while(!feof(FILE_web_linkfile)){ 		//对ls生成的文件中每个文件进行处理
			fscanf(FILE_web_linkfile,	"%s %s\n",url , type);

			int arraySize = (DownloadToolsArrNum + 1)*sizeof  (struct DownloadTools*);
			DownloadToolsArr =( struct DownloadTools **) realloc(DownloadToolsArr , arraySize);
			if(DownloadToolsArr==NULL){
				fprintf(stderr,"Realloc unsuccessful");
				exit(EXIT_FAILURE);
			}


			//没找到domain，那么开一个新节点
			DownloadToolsArr[DownloadToolsArrNum] = (struct DownloadTools*)malloc(sizeof( struct DownloadTools));
			p  =DownloadToolsArr[DownloadToolsArrNum]  ;
			strcpy(p->url , url);
			//const char *ToolsStr[]={"wget","PhantomjsWeb","PhantomjsAll ","ChromePythonWeb","ChromePythonAll","ChromeCommandWeb","ChromeCommandAll","ServerWeb","ServerAll"};
			if(0 == strcmp(type , "wget"))
				p->tools = ToolsWget;
			else if(0 == strcmp(type , "PhantomjsAll"))
				p->tools = ToolsPhantomjsAll;
			else if(0 == strcmp(type , "ChromePythonAll"))
				p->tools = ToolsChromePythonAll;
			else if(0 == strcmp(type , "ChromeCommandAll"))
				p->tools = ToolsChromeCommandAll;
			else if(0 == strcmp(type , "ServerAll"))
				p->tools = ToolsServerAll;
			else
				p->tools = ToolsWget;
			DownloadToolsArrNum++;
		}
		fclose(FILE_web_linkfile);
	}

	int i;
	for(i = 0 ;i <DownloadToolsArrNum ;i++){
		p = DownloadToolsArr[i];
		printf("%s  %d %s\n",p->url , p->tools ,ToolsStr[p->tools] );
	}
	sleep(3);
	return ;
}
*/
/**********************************************************************
//DownloadTools_Free
***********************************************************************/
void DownloadTools_Free(){
	int i;
	for(i = 0 ;i <DownloadToolsArrNum ;i++){
		free(DownloadToolsArr[i]);
	}
	free(DownloadToolsArr);
}



#define IsLink 100
int THREADINFO_Control_No=0;
int THREADINFO_Proxy_No =0;


char ErrorFile[500]="./errorfile.txt";


//#define NumMaxLayer 4 //最大层数 0-3
//#define NumWaitingQL 2   //最大等待队列数量
//#define NormalWaitingQL 1 //正常的队列
//#define ErrorWaitingQL 0     //错误等待队列编号
#define proxy_error 6
#define proxy_free 0
#define proxy_busy 2
//#define proxy_fail 11
struct PROXYTOTAL{
	int free;
	int add;
	int clear;
	int alive;

};
//定义代理服务器队列
typedef struct QNodeProxy{
	int  index;
	char proxy[25];
	//int   good[numgoodproxy];
	int *good;
	int tm;
	struct QNodeProxy* next;//指向下一个的指针
	//struct QNodeProxy* down;//指向向下的指针，用于存储坏代理节点
}QNodeProxy;

typedef struct QListProxy{
		struct QNodeProxy* front;
		struct QNodeProxy* end;

}QListProxy;

QListProxy *QLProxy,*QLProxyBad;//代理服务器队列
void InitQLProxy(QListProxy* QL)
{
    if(QL==NULL)
        QL=(QListProxy*)malloc(sizeof(QListProxy));
    QL->front=NULL;
    QL->end=NULL;
}


int  InsertQLProxy( QListProxy* QL,char *proxy  ,int numgoodproxy ,int  index)
{
	//广度遍历会造成节点数量巨大，深度遍历可以节省空间
	//插入一个任务
	QNodeProxy* p;
	p=(QNodeProxy*)malloc(sizeof(QNodeProxy));
	p->good=(int*)malloc(sizeof(int)*numgoodproxy);
	//p的一些初始化信息
	p->index = index;
	sprintf(p->proxy, "%s" , proxy);
	p->tm  =   time((time_t *) NULL);
	int i;
	for(i=0;i<numgoodproxy;i++)
	{
		p->good[i] = proxy_free;
	}

	if(QL->front==NULL)
	{
	    QL->front=p;
	    QL->end=p;
	    p->next=NULL;
	}
	else
	{
	    p->next=NULL;
	    QL->end->next=p;
	    QL->end=p;
	}

	return 1;

}

int  InsertQLProxysimple( QListProxy* QL,QNodeProxy* p)
{


	if(QL->front==NULL)
	{
	    QL->front=p;
	    QL->end=p;
	    p->next=NULL;
	}
	else
	{
	    p->next=NULL;
	    QL->end->next=p;
	    QL->end=p;
	}

	return 1;

}
int CountQLProxyOK( QListProxy* QL ,int numgoodproxy)
{
	int i=0,good ,numok=0;
	QNodeProxy*p;
	p=QL->front;

	while(p   )
	{

		for(i=0,good=0;i<numgoodproxy;i++)
		{
			if( p->good[i]  < proxy_error)  good++;
			//if(0 ==  p->good[i]   ){good =0; break;}
		}
		if(good == numgoodproxy) numok++;
		p= p->next;

	}
	return numok;



}
int WriteQLProxyFile( QListProxy* QL,int numgoodproxy  )
{

	char _proxyfilenamePath[200];
	sprintf(_proxyfilenamePath , "%s/proxy/lastproxy",NowWorkingDir);
	unlink(_proxyfilenamePath);

	FILE   *fp;
	fp=fopen(_proxyfilenamePath,"a+");
	int i=0,good ,numok=0;
	QNodeProxy*p;
	p=QL->front;

	while(p   )
	{

		for(i=0,good=0;i<numgoodproxy;i++)
		{
			if( p->good[i]  < proxy_error)  good++;

		}
		if(good == numgoodproxy) {
			fprintf(fp, "%s\n",  p->proxy);
			numok++;
		}
		p= p->next;

	}

	fclose(fp);
	return numok;

}
//*****************************************************
//删除代理服务器节点,采用移动的方法，不删除节点，避免造成程序中断
//*****************************************************
int ClearQLProxy( QListProxy* QL ,int numgoodproxy,struct PROXYTOTAL *proxy_total){
	proxy_total->alive =0 ;
	proxy_total->clear=0 ;
	int i=0,good ;
	QNodeProxy*p,*pleft;
	p=QL->front;

	while(p ){
		for(i=0,good=0;i<numgoodproxy;i++){
			 if(  p->good[i]  >= proxy_error)
			 	good++;
			 else
			 	break;
		}

		if(good == numgoodproxy  &&    time((time_t *) NULL) -  p->tm  > 20*60) {//20170128这里还是没有彻底解决问题，临时加的。
			//删除一个节点
			proxy_total->clear++;
			printf("--------ClearQLProxy------%d---\n" ,p->index);

			if( p == QL->front ){
				if(QL->front==QL->end){  //只有1个节点
					QL->front = NULL;
					QL->end = NULL;
					p->next = NULL;
					InsertQLProxysimple( QLProxyBad, p);
					/*
					free(p->good);
					p->good = NULL;
					free(p);
					p =NULL;
					*/
					break;
				}
				else{ //指向头节点，而且还有队列
					QL->front = p->next;
					//pnext = p->next ;
					//pleft = QL->front;

					p->next = NULL;
					InsertQLProxysimple( QLProxyBad, p);
					/*
					free(p->good);
					p->good=NULL;
					free(p);
					p =NULL;
					p = QL->front;
					*/
					p = QL->front;
					continue;
				}
			}
			else{//指向非头节点

				pleft->next = p->next;
				p->next = NULL;
				InsertQLProxysimple( QLProxyBad, p);
				/*
				free(p->good);
				p->good = NULL;
				free(p);
				p =NULL;
				*/
				p = pleft->next ;

				continue;
			}
		}
		else{
			proxy_total->alive++;
			pleft = p;
			p=p->next;
		}
	}
}
int checkproxy(char *proxy)
{
	//110.190.96.249:18186
	if(strlen(proxy)<9 || strlen(proxy)>25  ) return 0;
	int dian=0,maohao =0,digit=0;
	char *p;
	p = proxy;
	while(*p != '\0')
	{
		if(isdigit(*p))
		{
			digit=1;
		}
		else if( *p == '.')
		{
			dian =1;

		}
		else if( *p == ':')
		{
			maohao =1;

		}
		else
			return 0;

		 p++;

	}

	if(digit==1 && dian==1 && maohao==1  ) return 1;
	else return 0;

}


/*
int DeleteQLProxy(int myid,QListProxy* QL , QNodeProxy* porxynode )
{

	//删除一个任务
	//删除的节点有可能是线程当前节点下一个，所以要维护线程当前proxy节点
	//队列中没有节点，直接退出
	printf("%d\n" , CountQLProxy( QL));
	if(QL->front==NULL  )
	    return -1;

	QNodeProxy *p ;
	if(porxynode == QL->front)
	{
		if(porxynode == QL->end)
		{
			QL->front = NULL;
			QL->end = NULL;
		}
		else
			QL->front= porxynode->next;
	}
	else
	{
		p = QL->front;
		while(p   )
		{
		       if(p->next == porxynode)
		   	{
		   		if(porxynode == QL->end)
	   			{
					p->next	= NULL;
					QL->end = p;
	   			}
				else
					p->next = porxynode->next;
				break;
		   	}
			p=p->next;
		}
	}
	//porxynode->used = 99;
	printf("myid = %d   id=%d used=%d    CountQLProxy( QL)=%d\n" ,myid, porxynode->id ,porxynode->used ,CountQLProxy( QL));
	p = porxynode;
	free(p);
	porxynode = NULL;
	return 0;


}
*/
int DeleteQLProxy( QListProxy* QL   )
{
	//删除一个任务
	QNodeProxy *p;
	while(QL->front!=NULL){
		p=QL->front;
		if(QL->front->next==NULL){
			QL->front=NULL;
			QL->end=NULL;
		}
		else
		{
		    QL->front=p->next;
		}
		free(p->good);
		p->good = NULL;
		free(p);
		p=NULL;
	}
	free(QL);
	QL = NULL;

	return 0;

}
int DeleteQLProxyAll( QListProxy* QL   )
{
	//删除一个任务
	QNodeProxy *p;
	while(QL->front!=NULL)
	{
		p=QL->front;
		if(QL->front->next==NULL)
		{
		    QL->front=NULL;
		    QL->end=NULL;
		}
		else
		{
		    QL->front=p->next;
		}
		free(p);
		p= NULL;
	}
	free(QL);
	QL = NULL;
	return 0;

}
int  CountQLProxy(QListProxy* QL)
{	//遍历显示链表所有单元
    int i=0;
    QNodeProxy*p;
    p=QL->front;
    while(p   )
    {
        //printf("%d\t",p->link);
        i++;
        p=p->next;
    }
    return i;
}
int PrintQLProxy(QListProxy* QL)
{	//遍历显示链表所有单元
    int i=0;
    QNodeProxy*p;
    p=QL->front;
    while(p   )
    {
         printf("  %s\n",  p->proxy);
        i++;
        p=p->next;
    }
    return i;
}
//int Num_Download_Search = 0; //是否采集搜索引擎
//int Num_WeiBo_Search=0;//微博搜索的数量

/*
struct SEARCH_Structure	  //
{
	char web[100];	 //链接
	int   CaiJiIntervalTime;
	char searchlink_begin[200];
	char searchlink_end[200];
} SearchStructure[]= {
				  {"baidu", 10  ,   "http://news.baidu.com/ns?word=","&ie=gb2312&sr=0&cl=3&rn=20&tn=news&ct=0&clk=sortbytime"  },
				  {"sogou", 10  ,   "http://news.sogou.com/news?time=0&query=",""  },
				  {"soso", 10  ,   "http://news.soso.com/n.q?w=","&st=t"  },
				  {"youdao", 10  ,   "http://news.youdao.com/search?q=","&s=bytime&tr=no_range&keyfrom=search.bytime"  },
				  {"yahoo", 10  ,   "http://news.yahoo.cn/s?q=","&x=0-2-2-0"  },
				  {"bing", 10  ,   "http://cn.bing.com/news/search?q=","&FORM=BNFD"  }
		      } ;
int CaijiMore_Search_Num = sizeof(SearchStructure)/sizeof(struct SEARCH_Structure);  //求tag的数组个数
*/
/*
struct THREADINFOFENPEI
{
	int active;
	int type;
	int typetiny;
	int begin;
	int end;
} ThreadFenPei[]= {
				  {IsError,0,0, 0  ,  0 },
				  {IsWeb,0,0, 0  ,  0 },
				  {IsWeibo,0,0, 0  ,  0},
				  {IsWeiXin,0,0, 0  ,  0 },
	      } ;
int Num_ThreadFenPei= sizeof(THREADINFOFENPEI)/sizeof(struct ThreadFenPei);  //求tag的数组个数
*/

//unsigned long allwebnum=0;//采集网址的，所有的网址数量
unsigned int this_server_web_num=0;//采集网址
unsigned int this_server_WeiBo_num=0;//微博网址
unsigned int this_server_WeiXin_num=0;//微信

unsigned int this_server_CaijiMore_num=0;//频繁采集网址
unsigned int this_server_all_web_num=0; //这个服务器采集的所有网址总和，包括采集网址、微博网址、频繁采集网址

//unsigned long this_server_web_last_num=0;//剩余链接
unsigned int this_server_web_begin=0;
unsigned int this_server_web_end=0;

struct SERVER{ //存储链接和标题的数组结构
		unsigned int allwebnum;//采集网址的，所有的网址数量
		unsigned int web_num;//采集网址
		unsigned int WeiBo_num;//微博网址
		unsigned int CaijiMore_num;//频繁采集网址
		unsigned int all_web_num; //这个服务器采集的所有网址总和，包括采集网址、微博网址、频繁采集网址

		unsigned int web_last_num;//剩余链接
		unsigned int web_begin;
		unsigned int web_end;

		unsigned int BigLoop;
		//unsigned short MiddleLoop;
		unsigned int MiddleLoopBeginTime;
		//unsigned int   PublicWebNum;

		unsigned int zhanyong;
		unsigned int EnforceLinkLayerNum;
		unsigned int RepeatDownloadLinkLayerNum;
		unsigned int DownloadError;
		unsigned int MaxLoop;//最大圈数
		unsigned int badlinknum;
    } Server={0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1};







#define OneDaytm 24*3600
unsigned int  CaiJiClearDays;
unsigned int  CaiJiClearTime;//=2*24*3600;
unsigned int  BigLoopIntervalTime;//大圈间隔时间，单位是分钟，如果设置间隔一天，应设置为1380分钟而不是1440分钟，这样可以避免有时赶上某小时的最后时刻滑落300秒，而超过1440分钟
char RebootTime[10];//重启时间
#define loopsleep 60//*5

char Recordparselinkfile[500]="./recordparselinkfile";
char Myip[20];  //存储本机的IP地址




struct  QNodeWeb;


struct WEBINFOBASE
{ //存储网站的基本信息，替换数据库的存储
	unsigned int webid; //网站的ID号
	char link[1024];
	unsigned int layer; //这个网站要下载的层数
	char web[100];
	char kw[1024];
	unsigned int tinytype;
	char FileKw[1024];

	char ifout[50];//是否出域 in out
	char domain[100];
 };

typedef struct QNodeWeb
{
	unsigned int index; //网站在队列中的序号，测试用，可以删除
	unsigned int webid; //网站的ID号
	char *linkkw;//存储网址的网址或者关键词
	unsigned int layer; //这个网站要下载的层数
	//char *web;//[100];
	//unsigned int ifdomain;//是否可以出域采集 0 不可以，1 可以
	//char *domain;//主域名，http://www.sina.com.cn  =>sina.com.cn
	unsigned int ifout; //是否可以出域采集 yes no
	char domain[100];
	unsigned int mylock;

	unsigned int tm_last_download;
	//web是否要有loop，由于有新增网址，loop可以通过数据库查询知道这是新网址还是旧网址，
	//一个网址第一次采集时，是不下载终端页面的，只保留链接，一个网址二次采集时发现新链接就要下载，如果是终端连接要生成新文件，所以网址的loop极为重要
	//一个终端连接是否下载和web的loop紧密相连

	unsigned int   loop_web; //网站0表示未采集过，新添加网站默认值就是0，1表示采集过一圈。。。。。。,link的loop会继承这个定义
	//unsigned short int mylock;
	//unsigned int num_parselink;
	int download;

	unsigned short int tinytype; //(0是普通网站，1是可替换日期网站),微博(0是新浪，1是QQ),搜索引擎(代号0，1，2，3.。。。)
	//char *kw;//关键词
	unsigned int num_nodelink_working;//正在工作的下载节点
	struct QNodeShieldWeb *domainNode;//链接检查节点
	struct QNodeWebQueue *nodeWQ;//指向其他队列的节点的指针
	struct QNodeWeb* next;
	struct QNodeWeb* forward;//向前
}QNodeWeb;


typedef struct QListWeb
{
		struct QNodeWeb* front;
		struct QNodeWeb* end;

}QListWeb;


typedef struct QNodeThread
{
	struct THREADINFO *Thread;
	struct QNodeThread* next;
}QNodeThread;


typedef struct QListThread
{
		struct QNodeThread* front;
		struct QNodeThread* end;

}QListThread;


void InitQLThread(struct QListThread* QL)
{
    if(QL==NULL)
        QL=(struct QListThread*)malloc(sizeof(struct QListThread));
    QL->front=NULL;
    QL->end=NULL;
}

int InsertQLThread(struct QListThread* QL ,struct THREADINFO *Thread)
{
	QNodeThread *p;
	p=(QNodeThread*)malloc(sizeof(QNodeThread));

	p->Thread = Thread;

	if(QL->front==NULL)
	{
	    QL->front=p;
	    QL->end=p;
	    p->next=NULL;
	}
	else
	{
	    p->next=NULL;
	    QL->end->next=p;
	    QL->end=p;
	}

	return 1;
}
int DeleteQLThread( struct QListThread* QL   )
{
	//删除一个任务
	QNodeThread*p;
	while(QL->front)
	{
		p=QL->front;
		if(QL->front->next==NULL)
		{
		    QL->front=NULL;
		    QL->end=NULL;
		}
		else
		{
		    QL->front=p->next;
		}
		free(p);
		p= NULL;
	}
	free(QL);
	QL = NULL;
	return 0;

}



MYSQL *mysql_conn_init(char *database)
{

	char *server = "localhost";
	char *user = "root";
	char  password[100];
//	char sock_name[100];
/*
	if(strstr(Myip,".49")  )sprintf(password , "2caa6884339980cae91ff273275a5129owck") ;
	else   sprintf(password , "54eb0d6c977248ad408f367cfda063e4") ;
*/

	char *sock_name = NULL;
/*
	if(strstr(Myip,".49")  )
		{
			sprintf(password , "2caa6884339980cae91ff273275a5129owck") ;
			char aaaa[100];
			sprintf(aaaa,"%s", "/tmp/mysql.sock");
			sock_name = aaaa;
		}
	else   sprintf(password , "54eb0d6c977248ad408f367cfda063e4") ;
*/
	sprintf(password , "54eb0d6c977248ad408f367cfda063e4") ;
/*
	if(strstr(Myip,".49")  )
		{
			sprintf(password , "2caa6884339980cae91ff273275a5129owck") ;
			sprintf(sock_name,"%s", "/tmp/mysql.sock");
		}
	else
		{
			sprintf(password , "54eb0d6c977248ad408f367cfda063e4") ;
			sock_name[0] = '\0';
		}
  */
	//static char *database = "manzhua";
	//char *sock_name = NULL; // "/var/lib/mysql/mysql.sock";
	int port = 3306;
	char *sql;
	MYSQL *conn;

	conn = mysql_init (NULL);
	/* Connect to database */
	if (!mysql_real_connect (conn, server, user, password, database, port, sock_name, 0)) //0  CLIENT_MULTI_RESULTS  CLIENT_MULTI_STATEMENTS
	{
		fprintf (stderr, "%s\n", mysql_error (conn));
		mysql_close(conn);
		return NULL;
	}
	mysql_query (conn, "set names gbk");
	//mysql_free_result(mysql_store_result(conn));

	//mysql_query(conn,"set wait_timeout = 24*3600");
	//mysql_free_result(mysql_store_result(conn));

	//mysql_query(conn, "set interactive_timeout=24*3600");
	//mysql_free_result(mysql_store_result(conn));


	//mysql_real_query(conn, nowsql ,strlen(nowsql));
	return conn;
}
int write_database_error(MYSQL *conn ,char *message ,char *sql)
{

	char buf[2000];
	sprintf(buf , "\n %s:\n%s\n%s\n\n" ,message,sql ,mysql_error(conn));
	printf("%s\n",buf);
	write_error(buf);
	return 0;
}


int writeDatabaseError(MYSQL *conn ,char *message ,char *sql ,int ifprint)
{
	char buf[2000];
	sprintf(buf , "\n %s:\n%s\n%s\n\n" ,message,sql ,mysql_error(conn));
	if(1 == ifprint)
		printf("%s\n",buf);
	write_error(buf);
	return 0;
}



//----------------------------多线程都头------------------------------------
#ifdef __Linux__
 #  define _REENTRANT
 #  define _POSIX_SOURCE
#endif

 /* Hack for LinuxThreads */
#ifdef __Linux__
#  define _P __P
#endif

#include <pthread.h>
//等待队列锁，有关等待队列的所有操作都要上锁
//pthread_mutex_t mymutex_QLWgetWaiting=PTHREAD_MUTEX_INITIALIZER;
//网址队列锁
pthread_mutex_t mymutex_web=PTHREAD_MUTEX_INITIALIZER;


//pthread_mutex_t mymutex_wget_waiting_all=PTHREAD_MUTEX_INITIALIZER;
//pthread_mutex_t mymutex_wget_depth=PTHREAD_MUTEX_INITIALIZER;
//pthread_mutex_t mymutex_sh_working=PTHREAD_MUTEX_INITIALIZER;
pthread_mutex_t mymutex_num_nodelink_working=PTHREAD_MUTEX_INITIALIZER;
pthread_mutex_t mymutex_loop_thread_max=PTHREAD_MUTEX_INITIALIZER;
pthread_mutex_t mymutex_check_web_loop=PTHREAD_MUTEX_INITIALIZER;

pthread_mutex_t mymutex_good_index_proxy=PTHREAD_MUTEX_INITIALIZER;
//-----------------------------------------------------------------------------

int   IfOut;

int   ServerQueue ; //y=(x+1)%10
int   ServerNum;

int timeout=3;
int PubLayer=1;//公共的采集深度
//int Num_Thread ;
//int Num_Download_Web; //下载线程数
int Num_FirstWork=1; //处理后续工作线程数
int Num_Download_Proxy=1;
int Num_Download_Error=1;

int Time_download = 3600*6;
//int WgetTimeOut ;//wget超时时间

char Tmppath[500]; //临时文件夹
char Targetdir[500];  //目标文件夹
char Savedir[500]; //存储网址现在信息的文件夹
char Downdloadip[50]; //下载关键的词的服务器地址
int Port;//端口号
char Wget_DownLoad_Dir[500];


char Mywget[200] =  "/home/zran/src/wget/src/wget";
char Wgetreject[500]="--reject=gif,jpg,jpeg,avi,rmvb,rar,gz,tar,png,css,js,swf,bmp,doc,docx,pdf,exe,mp3,ppt,pptx,xls,xlsx,rtf,iso,apk";
char Errorfile[500]="./error.manzhua";
char Recordworkfile[500]="./work.manzhua";
int  Outtime=3600*5;
char Parseddir[500];//="/estar/parsed/";



typedef struct QNodeMd5
{
	char md5[MD5_DIGEST_LENGTH*2+1];
	struct QNodeMd5* next;
}QNodeMd5;

struct QListMd5
{
		struct QNodeMd5* front;
		struct QNodeMd5* end;

} ;
void InitQLMd5(struct QListMd5* QL)
{
    if(QL==NULL)
        QL=(struct QListMd5*)malloc(sizeof(struct QListMd5));
    QL->front=NULL;
    QL->end=NULL;
}

int InsertQLMd5(struct QListMd5* QL ,char *md5)
{
	QNodeMd5 *p;
	p=(QNodeMd5*)malloc(sizeof(QNodeMd5));

	sprintf(p->md5,"%s",md5);

	if(QL->front==NULL)
	{
	    QL->front=p;
	    QL->end=p;
	    p->next=NULL;
	}
	else
	{
	    p->next=NULL;
	    QL->end->next=p;
	    QL->end=p;
	}

	return 1;
}
int DeleteQLMd5( struct QListMd5* QL   )
{
	//删除一个任务
	QNodeMd5*p;
	while(QL->front)
	{
		p=QL->front;
		if(QL->front->next==NULL)
		{
		    QL->front=NULL;
		    QL->end=NULL;
		}
		else
		{
		    QL->front=p->next;
		}
		free(p);
		p = NULL;
	}
	free(QL);
	QL = NULL;
	return 0;

}
int find_in_QLMd5(struct QListMd5* QL ,char *md5)
{
	QNodeMd5 *p=QL->front;

	while(p)
	{
		if(0 == strcmp(p->md5, md5) )
			return 1;
		p = p->next;

	}
	return 0;
}

struct LINKTITLE{ //存储链接和标题的数组结构
          char link[5000];
          char title[5000];
	    char md5[MD5_DIGEST_LENGTH*2+1];
	    int layer;
    } ;


//WGET节点
typedef struct QNodeLink
{
	//int index;
	char *linknew;
	char *titlenew;
	unsigned int layer; //这个网站要下载的层数
	char md5[MD5_DIGEST_LENGTH*2+1];
	char md5_father[MD5_DIGEST_LENGTH*2+1];
	unsigned short int web_or_link;//是链接，还是网站，涉及是否要释放问题
	unsigned int parselinknum;
	unsigned int begin_wget_download_tm; //这个链接开始下载的开始时间戳
	//unsigned int last_wget_downlaod_tm;//最近一次对此链接的采集时间戳
	int query_return;//锁定link时返回值
	int download_link;//link下载后的结果，-100一下不要，。。。。
	int download_database;//download_link_last;//数据库中数据
	unsigned int size_last; //下载的网页大小，指数据库中的存储的大小
	//unsigned int num_download;//采集的次数，主要给处理坏节点使用
	unsigned int ifdownloaded;//是否下载了
  	//继承父亲的信息
  	unsigned int loop_link;//
  	unsigned int index;
	unsigned int loop_link_father;//

	QNodeWeb   *node_web;//指向网站队列节点的指针
	QNodeProxy *node_proxy;//指向代理服务器队列的节点
	struct THREADINFO *threadinfo;

	unsigned int tools;//下载这个链接的工具，server,wget......

	struct QNodeLink* next;

	char SNUID[33];//cookie
}QNodeLink;

struct QList
{
		struct QNodeLink* front;
		struct QNodeLink* end;

} ;
void InitQL(struct QList* QL)
{
    if(QL==NULL)
        QL=(struct QList*)malloc(sizeof(struct QList));
    QL->front=NULL;
    QL->end=NULL;
}


#define  SHWaiting	0	//等待中
#define  SHWorking	1	//工作中
#define  SHAdding	2	//装弹中


//SH节点
typedef struct QNodeSH
{
	//unsigned  int  type; //类型
	unsigned  int  index;
	unsigned  int  numcheck;
	unsigned  int  working; //0是等待，1是工作，2装弹中
	char shfilename[100];
	//FILE *FILE_SH;
	unsigned  int  num_wget;//这个sh文件中wget数量
	struct QList *QLWget;
	struct QNodeSH* next; //向后
	struct QNodeSH* forward;//向前
}QNodeSH;

typedef struct QListSH
{
		struct QNodeSH* front;
		struct QNodeSH* end;

}QListSH;

struct LOOP_NUM{
	//线程小圈统计

	//web
	  int web_add;  //每圈新增网站数量

	//wget
	  int wget_new_run; //本圈新开始wget下载任务

	  int wget_working_all;//队列中wget正在下载的节点数量，由下载和判断下载工作，两地决定，动态，不可没小圈清零。
	  int wget_waiting_all;
	 int wget_depth;//大深度的数量，比如2，3.。。。。。。。
	//sh
	  int sh_add;//没圈增加的SH文件数量
	  int sh_working;

	//link
	  int link_download;
	  int link_download_ok;
	  int link_okwrited;
	  int link_okwrited_total;//用于统计
	  int link_parse;//解析的不重复链接
	  int link_parse_new;//发现的新链接
	  int link_bad;
	  int link_insert;

	//tm
	  int tm_work_begin;//loop_begin_tm

} ;




struct CONFIGSET{

	//配置文件读取信息
	unsigned int num_thread;//采集的线程数量
	unsigned  int type; //队列的类型网站、搜索引擎，基本就这2种类型 IsWeb  IsSearch   //0是网站，1是微博，2是搜索引擎采集网址 , 100是网址
	unsigned  int IfDownload;//是否下载网址和关键词文件
	//unsigned  int Proxy; //是否使用代理服务器，Proxy_no ,Proxy_web,Proxy_all
	unsigned  int Connection;//连接方式
	char webServer[100];//web服务器地址

	unsigned  int Tools;
	char FileWeb[200];//网址文件
	//char FileKw[200]; //关键词文件
	unsigned  int ServerNum;//几个服务器参与采集
	unsigned  int ServerOrder;//参与采集服务器中排序号
	unsigned  int NumSHInThread; //一个线程中sh文件个数，也是ThreadWgetMaxnum
	unsigned  int NumWgetInSH;   //sh文章中wget数量MaxwgetnumInSh
	unsigned  int IntervalTimeWeb; //同一个网址采集间隔
	unsigned  int WgetTimeOut; //wget超时时间

} ;
//网址队列
typedef struct QNodeWebQueue
{
	//struct QListWebAll WebQueue;


	unsigned int  index; //队列编号
	unsigned int webid_pub;//webid , 不是roleid
	char link[200];//主要存储引擎的公共链接
	char web[100];//存储公共web
	unsigned int myid_begin;//线程号开始

	int index_proxy;//指向地理服务器的good字段的顺序号，-1是不使用，>-1表示使用
	 unsigned  int loop_WQ;//队列采集的几圈
	 unsigned  int loop_thread_max;//当前线程循环的最大数
	//unsigned  int loop_num_done;//这圈已经处理了多少个链接，线程共享更新

	struct QListWeb *QLWeb;
	char *QLWebPub_buf ; //存储链接或关键词的缓存
	char *QLWebPub_link_p ;

	//char *QLWebPub_web ; //存储网址关键词的缓存，也是存储主域名的空间
	//char *QLWebPub_web_p ;//这是一个临时指针，再分配QLWebPub_web内存时用
	//统计信息
	unsigned  int num_web;//队列中的站点数量
	unsigned  int num_web_valid;//有效的网址数量
	unsigned  int num_web_working;//工作中的web数量
	struct LOOP_NUM LoopQueue;//线程针对队列的统计信息
	//unsigned  int num_sh_public;//
	struct QNodeWebQueue* next;

	//配置文件读取信息
	struct CONFIGSET config;
	unsigned int num_thread;//采集的线程数量
	unsigned  int type; //队列的类型网站、搜索引擎，基本就这2种类型 IsWeb  IsSearch   //0是网站，1是微博，2是搜索引擎采集网址 , 100是网址
	unsigned  int IfDownload;//是否下载网址和关键词文件
	//unsigned  int Proxy; //是否使用代理服务器，Proxy_no ,Proxy_web,Proxy_all
	unsigned  int Connection;//连接方式
	unsigned  int Tools;
	char webServer[100];//提供web服务的地址
	char FileWeb[200];//网址文件
	char FileKw[200]; //关键词文件
	unsigned  int ServerNum;//几个服务器参与采集
	unsigned  int ServerOrder;//参与采集服务器中排序号
	unsigned  int NumSHInThread; //一个线程中sh文件个数，也是ThreadWgetMaxnum
	unsigned  int NumWgetInSH;   //sh文章中wget数量MaxwgetnumInSh
	unsigned  int IntervalTimeWeb; //同一个网址采集间隔
	unsigned  int WgetTimeOut; //wget超时时间
	char kw_replace[100];//替换关键词
	unsigned  int NumDownloadError;//这个队列下载文件失败的次数，次数超过某个阈值就重启拨号，更新ip
	//统计信息
	//unsigned  int loop_begin_tm;//每个圈开始时间

	//struct QListThread *QLThread;
	//struct QList* QLWgetWaiting;
	unsigned  int always_download;//无论什么情况这个队列的link都下载

	//指向多个线程的动态数组
	unsigned  int threadsNum;
	struct THREADINFO **threads;

}QNodeWebQueue;

typedef struct QListWebQueue
{
		struct QNodeWebQueue* front;
		struct QNodeWebQueue* end;
}  QListWebQueue;

QListWebQueue  *QLWebAll;//网址大队列

void InitQLWebQueue(struct QListWebQueue* QL)
{
    if(QL==NULL)
        QL=(struct QListWebQueue*)malloc(sizeof(struct QListWebQueue));
    QL->front=NULL;
    QL->end=NULL;
}
struct QNodeWebQueue*  InsertQLWebQueue( QListWebQueue* QL ,struct CONFIGSET *config,   struct MYNUM * Num ,struct WEBINFOBASE * webinfo  )
{
	struct QNodeWebQueue* nodeWQ;
	nodeWQ=(QNodeWebQueue*)malloc(sizeof(QNodeWebQueue));

	InitQLWebAll( nodeWQ   , Num , config  ,webinfo);
	//插入一个任务


	if(QL->front==NULL)
	{
	    QL->front=nodeWQ;
	    QL->end=nodeWQ;
	    nodeWQ->next=NULL;
	}
	else
	{
	    nodeWQ->next=NULL;
	    QL->end->next=nodeWQ;
	    QL->end=nodeWQ;
	}

	return nodeWQ;

}
int DeleteQLWebQueue( struct QListWebQueue* QL   )
{
	//删除了所有队列
	QNodeWebQueue *nodeWQ;
	while(QL->front!=NULL)
	{
		nodeWQ=QL->front;
		if(QL->front->next==NULL)
		{
		    QL->front=NULL;
		    QL->end=NULL;
		}
		else
		{
		    QL->front=nodeWQ->next;
		}
		DeleteQLWeb(nodeWQ->QLWeb);

		free(nodeWQ->QLWebPub_buf );
		nodeWQ->QLWebPub_buf=NULL;
		nodeWQ->QLWebPub_link_p=NULL;

		//free(nodeWQ->QLWebPub_web );
		//nodeWQ->QLWebPub_web =NULL;
		//nodeWQ->QLWebPub_web_p=NULL;
		//free(nodeWQ->QLWebPub_kw );

		//DeleteQLThread(nodeWQ->QLThread);
		//DeleteQLAll(nodeWQ->QLWgetWaiting);

		free(nodeWQ->threads);
		nodeWQ->threads = NULL;

		free(nodeWQ);
		nodeWQ = NULL;


	}

	free(QL);
	QL = NULL;

	return 0;

}
void InitQLWebQueue_NumDownloadError( struct QListWebQueue* QL   )
{
	//初始化所有队列的NumDownloadError值
	QNodeWebQueue *nodeWQ = QL->front;
	while(nodeWQ){
		nodeWQ->NumDownloadError = 0;
		nodeWQ = nodeWQ->next;
	}
}

/*
void freeQNodeLink(struct QNodeLink* p)
{
	if(
		       p->linknew &&
		    ( p->web_or_link == IsLink ||
			IsWeb == p->node_web->nodeWQ->type    &&  IsReplaceWeb == p->node_web->tinytype ||
			IsWeb != p->node_web->nodeWQ->type  )
	  )
		free(p->linknew);

	if(p->titlenew) free(p->titlenew);

	free(p);
	p= NULL;
}
*/

void freeQNodeLink(struct QNodeLink* p)
{
	if( IsWeb == p->web_or_link  )  //网址
	{
		if( IsWeb== p->node_web->nodeWQ->type )  //普通网址采集
		{
			if(IsReplaceWeb ==  p->node_web->tinytype ) //需要替换关键词的
			{
				free(p->linknew);
				p->linknew = NULL;
			}
		}
		else //微博搜索引擎等需要替换关键词的
		{
			free(p->linknew);
			p->linknew = NULL;
		}
	}
	else //链接
	{
		free(p->linknew);  //***************20170127
		p->linknew = NULL;
	}

	//标题
	if(p->titlenew)
	{
		free(p->titlenew);
		p->titlenew = NULL;
	}

	free(p);
	p= NULL;
}



#define  md5num 2000
#define  md5_buf_size   (MD5_DIGEST_LENGTH*2+1)*(md5num+2)

struct CREATEDIR{
	unsigned  int index;//创建存在网页的目录数字
	unsigned  int filenum;
	unsigned  int tm_lastmkdir;//上一次创建目录的时间
	char _targetdir[200]; //合成的目标目录
	char targetdir[200];   //合成的目标目录

};
struct THREADINFO{ //存储链接和标题的数组结构

				   int myid; //线程号
		unsigned  int loop_thread;//线程针对队列采集了多少圈
		unsigned  int node_link_index;
		struct CREATEDIR CreatDir;//建立生成好的文件存储的目录

		struct LOOP_NUM LoopThreadSmall; //线程每个小扫描循环的统计信息
		struct LOOP_NUM LoopThread; //线程每扫描队列一次的信息统计

		struct LOOP_NUM LoopBig;//大循环通常是24小时

		struct QList* QLWgetWaiting;  // 2个队列，0号正常采集，1号一个错误队列
		//struct QList* QLWgetWaiting_error; //错误队列

		QNodeWeb* node_web_new;//这个线程最近采集的网站

	 	QListSH *QLTaskSH_waiting;//sh任务队列
		QListSH *QLTaskSH_working;
		//wget工作
		char WgetWorkDir[200]; //wget工作目录
		char _son_wget_info[200];
		char _wget_html[200];
		char wget_html[200];


		char order_all[2000];//命令缓存
		//char md5_buf[md5_buf_size];

		QNodeProxy *node_proxy;//指向代理服务器地址
		struct QNodeWebQueue *nodeWQ;

		 int tm_add_web_last;//添加网站的时间

		 //struct QNodeThread *node_thread_WQ;
		 MYSQL *conn;
} ;


#define errexit(code,str)                          \
   fprintf(stderr,"%s: %s\n",(str),strerror(code)); \
   exit(1);


int TotalQLWebQueue( struct QListWebQueue* QL   ){
  int num = 0 , i;
  char buffer[500];
  char nowtime_str[100];
  Mytime(nowtime_str);
  char *p =index(nowtime_str , ' ');
  *p ='\0';

  QNodeWebQueue *nodeWQ=QL->front;
  while(nodeWQ){
	  num = 0 ;
	  for(i =-0 ;i <nodeWQ->threadsNum ;i++){
		  num = num +nodeWQ->threads[i]->LoopBig.link_okwrited_total;
		  nodeWQ->threads[i]->LoopBig.link_okwrited_total = 0;
	  }
	  sprintf(buffer , "/home/zran/src/wget/src/wget -q  -O    %s/total.txt  \"http://www.estar360.com/system/servers.php?&myip=%s&date=%s&num=%d&part=manzhua&type=%s\"	& ", NowWorkingDir, Myip,nowtime_str ,num,typestr[nodeWQ->type]);
	  printf("%s\n" ,buffer);
	  system(buffer);

	  nodeWQ = nodeWQ->next;
  }

  return 0;
}

//----------------------------------------------------------------------
void malloc_cp(char *src ,char *target)
{
		target = (char *)malloc(strlen(src)+1);
		sprintf(target,"%s" ,src);

}
#define LinkNew 2     	//新链接，并已经锁定
#define Link_Locked 1 	//老链接，并已经锁定
#define Link_Unlock 0	//老链接，未锁定成功
#define LinkError -1 	//数据库错误

#define IsNewLink 1
#define IsOldLink 0
int lock_web_md5 (  struct QNodeLink *nodelink ,  QNodeWebQueue *nodeWQ,struct QNodeWeb *node_web)
{

		//-1 是数据库错误
		//  0 别的线程已经锁定
		//  1 老链接 锁定了
		//  2  新链接锁定
		//UPDATE `manzhua`.`web_md5` SET `mylock`='%d'  ,`order`='%d' WHERE  `mylock` <1  AND `type`=%d  %s AND `download`>0 AND `loop`<'%d'  ORDER BY  `web_md5`.`tm` ASC , `web_md5`.`loop` ASC    LIMIT 1

		//nodelink->web_or_link= IsWeb;
		//nodelink->titlenew =NULL; //linkinfo->title[0] = '\0';
		//nodelink->layer =node_web->layer;
		//nodelink->loop = node_web->loop;
		//nodelink->parselinknum  = node_web->parselinknum;
		//nodelink->download_database = node_web->download; //*****************************




		//常规网址
		if(nodelink->node_web->nodeWQ->type== IsWeb)  //if(webinfo->type == IsWeb)
		{
			md5_gen_link(nodelink->md5, node_web->linkkw);
			//可替换的常规地址，需要替换时间
			if(nodelink->node_web->tinytype   == IsReplaceWeb)
			{
				nodelink->linknew = (char *)malloc(strlen(node_web->linkkw)+1);
				sprintf(nodelink->linknew,"%s" ,node_web->linkkw);

				//Y-m-d
				char estar_YYYY[5],estar_mm[3],estar_dd[3];
				struct tm *tm_ptr;
				time_t the_time;
				(void) time(&the_time);
				tm_ptr=localtime(&the_time);
				sprintf(estar_YYYY,"%02d",(tm_ptr->tm_year+1900));
				sprintf(estar_mm,"%02d",tm_ptr->tm_mon+1);
				sprintf(estar_dd,"%02d",tm_ptr->tm_mday);

				ReplaceStr(nodelink->linknew  ,"estar_YYYY", estar_YYYY);
				ReplaceStr(nodelink->linknew  ,"estar_mm", estar_mm);
				ReplaceStr(nodelink->linknew  ,"estar_dd", estar_dd);
				printf("myid =%d   link estar replace [%s]\n" ,nodelink->threadinfo->myid,nodelink->linknew);
			}
			//常规网址
			else
				nodelink->linknew = node_web->linkkw;
		}
		//关键词合成链接
		else {
				nodelink->linknew = (char *)malloc(strlen(nodeWQ->link) + strlen(node_web->linkkw)+1);
				//sprintf(nodelink->linknew,"%s%s" ,nodeWQ->link,node_web->kw);
				sprintf(nodelink->linknew,"%s" ,nodeWQ->link );
				ReplaceStr(nodelink->linknew , nodeWQ->kw_replace , node_web->linkkw);
				//printf("lock_web_md5[%s]\n",nodelink->linknew);
				md5_gen_link(nodelink->md5, nodelink->linknew);
		}

		sprintf(nodelink->md5_father,"%s" , nodelink->md5);
		return 1;



}


 int unlock_web_md5( struct QNodeWeb *node_web ,int loop_thread,int ifchange)
{
	if(1 == ifchange)
	{
		 node_web->tm_last_download = time((time_t *) NULL);

		 node_web->loop_web  = loop_thread;

		 //node_web->loop_web++;
		 //if( node_web->loop_web <   node_web->nodeWQ->loop_WQ)
		//	 node_web->loop_web =  node_web->nodeWQ->loop_WQ;
	}

	//返回1表示存在，返回0表示不存在.查询链接表，是否有这个链接的MD5，无就插入
	node_web->mylock = 0;
	//node_web->download = download;// nodelink->download_link;

	return 1;


}

int write_error(const char *message)
{
	char buf[2000];
	sprintf(buf,"%s",message);
	//printf("%s\n",buf);
	Recordwork(buf,ErrorFile);
	return -1;
}
struct LINKDATABASE{
		unsigned int tm;
		unsigned int download;
		unsigned int loop;
				int mylock;
				int layer;
	     unsigned int web_or_link;
	     unsigned int size_last;
} ;

int insert_web_md5_no(MYSQL *conn,   char *md5 ,int index)
{
	//返回1表示存在，返回0表示不存在.查询网站表，是否有这个链接的MD5，无就插入

	char sql[1000];
	sprintf(sql, "INSERT INTO `manzhua`.`web_md5_no` ( `md5` ,  `index`) VALUES ( UNHEX( '%s' ) ,%d)", md5,index);
	if (mysql_query (conn, sql))
	{
		//mysql_free_result(mysql_store_result(conn));
		printf("insert_web_md5_no  error  %s \n",sql);
		return 1;
    }
	//mysql_free_result(mysql_store_result(conn));
	return 0;
}
int lock_linkmd5(MYSQL *conn,  struct QNodeLink *nodelink  ,int web_or_link)
{
	char sql[500];



	//sprintf(sql,"UPDATE `manzhua`.`link_md5` SET `mylock` = '%d',`layer` = '%d',`web_or_link` = '%d' WHERE `link_md5`.`md5` = CAST( 0x%s AS BINARY ) LIMIT 1",nodelink->threadinfo->myid, nodelink->layer ,nodelink->web_or_link,nodelink->md5 );
	sprintf(sql,"UPDATE `manzhua`.`link_md5` SET `mylock` = %d,`layer` = %d,`web_or_link` = %d WHERE `link_md5`.`md5` = CAST( 0x%s AS BINARY ) LIMIT 1",nodelink->threadinfo->myid, nodelink->layer , web_or_link,nodelink->md5 );

	if (mysql_query (conn, sql))   { write_database_error( conn ,"lock_linkmd5:" ,sql); return -1; } //数据库错误，返回-1

	if(mysql_affected_rows(conn) > 0)
	{
		//mysql_free_result(mysql_store_result(conn));
		return Link_Locked;
	}
	else
	{
		//mysql_free_result(mysql_store_result(conn));
		printf("lock_linkmd5 error---------------------------------------\n%d  [%s]\n",nodelink->threadinfo->myid ,sql);
		return Link_Unlock;
	}


}
int insert_linkmd5(MYSQL *conn,  char *md5, int myid, int layer,int loop_link,int download_database,int web_or_link,char *link)
{
	char sql[500];


	//nodelink->loop_link= 0;//在这个加时最合理的
	//sprintf(sql, "INSERT INTO `manzhua`.`link_md5`  (`md5`,`mylock`,`layer`,`loop`,`download`,`web_or_link`)  VALUES (UNHEX('%s') ,%d ,%d,%d,%d,%d)",   nodelink->md5, nodelink->threadinfo->myid, nodelink->layer,nodelink->loop_link,nodelink->download_database,nodelink->web_or_link);
	sprintf(sql, "INSERT INTO `manzhua`.`link_md5`  (`md5`,`mylock`,`layer`,`loop`,`download`,`web_or_link`)  VALUES (UNHEX('%s') ,%d ,%d,%d,%d,%d)",   md5, myid, layer,loop_link,download_database,web_or_link);
	if (mysql_query (conn, sql))
	{
		char buf[2000];
		sprintf(buf,"insert_linkmd5:[%s]",link);
		//write_database_error( conn ,buf,sql);
		writeDatabaseError( conn ,buf,sql,0);
	 	if(1062 == mysql_errno (conn)) {
			//mysql_free_result(mysql_store_result(conn));
			return Link_Unlock;  //链接刚刚被别的线程插入，返回0，的确存在这种情况。
	 	}
		else{
			//mysql_free_result(mysql_store_result(conn));
			return LinkError;  //其他错误，返回-1
		}
	}
	else
	{
		//mysql_free_result(mysql_store_result(conn));
		return LinkNew; //新链接返回2
	}


}
int update_tm_linkmd5(MYSQL *conn,  struct QNodeLink *nodelink ,struct LINKDATABASE *linkdatabase  )
{
	//更新链接时间戳
	if(0 == linkdatabase->mylock &&   time((time_t *) NULL)- linkdatabase->tm > OneDaytm    ) //如果链接存在而且24小时没更新时间戳了，那么就更新一下，避免清理链接时被清理掉,也没必要每次都更新，耗费资源
	{
		char sql[500];
		sprintf(sql,"UPDATE `manzhua`.`link_md5` SET `tm` = Now()   WHERE `link_md5`.`md5` = CAST( 0x%s AS BINARY ) LIMIT 1", nodelink->md5 );
		if (mysql_query (conn, sql))   {
			write_database_error( conn ,"lock_link_md5:" ,sql);
			//mysql_free_result(mysql_store_result(conn));
			return LinkError;
		} //数据库错误，返回-1
		//mysql_free_result(mysql_store_result(conn));
	}
	return Link_Unlock;

}
int update_link_md5(  MYSQL *conn,char *md5,char * field, int data)
{

	char sql[500];
	sprintf(sql,"UPDATE `manzhua`.`link_md5` SET `%s` = %d ,`mylock` =  '0'   WHERE `link_md5`.`md5` = CAST( 0x%s AS BINARY ) LIMIT 1",field, data, md5 );
	if (mysql_query (conn, sql))   {
		write_database_error( conn ,"update_link_md5:" ,sql);
		//mysql_free_result(mysql_store_result(conn));
		return LinkError;
	} //数据库错误，返回-1
	//mysql_free_result(mysql_store_result(conn));
	return Link_Unlock;
}
/*
int have_link_md5(MYSQL *conn,char *md5,int BigLoop )
{
	if(1 == BigLoop)
		return 0;
	else
	{
		char sql[500];
		int num;
		MYSQL_RES *res ;
		sprintf(sql, "SELECT   `mylock` FROM   `manzhua`.`link_md5` WHERE `link_md5`.`md5` = CAST( 0x%s AS BINARY )    LIMIT 1", md5  );
		if (mysql_query ( conn, sql))
		{
			 return 0;
	    	}
		res = mysql_store_result(conn);
		num = mysql_num_rows(res);
		mysql_free_result(res);
		return num;
	}
}
*/
 int read_database_info(MYSQL *conn,char *md5, struct LINKDATABASE *linkdatabase)
{
		int myreturn =0;
		if( BigLoop >1)
		{
				char sql[500];
				MYSQL_RES *res;
				MYSQL_ROW row;
				//nodelink->repeat = 0;
				sprintf(sql, "SELECT   UNIX_TIMESTAMP(`tm`) ,`mylock`,`layer`,`download`,`loop`,`web_or_link`  FROM  `manzhua`.`link_md5` WHERE `link_md5`.`md5` = CAST( 0x%s AS BINARY ) LIMIT 1",  md5 );

				if (mysql_query (conn, sql))  { write_database_error( conn ,"lock_link_md5:" ,sql); return -1; }  //数据库错误，返回-1
				res = mysql_store_result(conn);
				if(row = mysql_fetch_row(res))
				{

						linkdatabase->tm =  		atoi(row[0]);//strtoul (row[0], NULL, 0);
						linkdatabase->mylock =		atoi(row[1]);//strtoul (row[1], NULL, 0);
						linkdatabase->layer =		atoi(row[2]); //strtoul (row[2], NULL, 0);
						linkdatabase->download =	atoi(row[3]);//strtoul (row[3], NULL, 0);
						linkdatabase->loop  =		atoi(row[4]);//strtoul (row[4], NULL, 0);
						linkdatabase->web_or_link =	atoi(row[5]);//strtoul (row[5], NULL, 0);

						//更新web_or_link ????
						myreturn =1;
				}

				mysql_free_result(res);res = NULL;
		}

		return myreturn;
}


 int unlock_link_md5(MYSQL *conn,  struct    QNodeLink *nodelink )
{

	//---------------------------------------------------------------------------------------------------

	if(
		     Download_OKForever == nodelink->download_database //曾经的永久链接，就认为是永久链接吧
		||  Download_OKTrue == nodelink->download_link    //如果这次采集成功就升级为永久好链接
		||  nodelink->node_web->nodeWQ->type != IsWeb   //搜索引擎，微博，等都认为是永久好链接
		||  nodelink->node_web->nodeWQ->type== IsWeb && nodelink->node_web->tinytype == IsReplaceWeb  //替换网址也认为是永久好链接
	 )
	{
		nodelink->download_database = Download_OKForever;//永久好链接
	}
	else
	{

		if(nodelink->download_link < Download_Line  )
		{
			if(Download_TooBig == nodelink->download_link || Download_Undetermined == nodelink->download_database) //一个链接多次采集结果是坏链接，那么久永久定性为坏链接
				nodelink->download_database = Download_BadForever;
			else
				nodelink->download_database = Download_Undetermined;
		}
		else
		{
			//第一次下载时，很多末级练级不下载，默认Download_OKInit
			//printf("MMMMMMMMMMMMMMMMMMMMMMMMMMMMMM nodelink->download_link=%d \n" ,nodelink->download_link );
			nodelink->download_database = nodelink->download_link ;
		}

	}

	//必须锁定nodelink->layer，避免深度采集的任务别放弃
	char sql[500];
	if(1== nodelink->ifdownloaded)
		sprintf(sql, "UPDATE `manzhua`.`link_md5`  SET `mylock`='0' ,`download`='%d' ,`loop`='%d' ,`size_last`='%d'  WHERE `link_md5`.`md5` = CAST( 0x%s AS BINARY ) AND `mylock`='%d' AND `layer`='%d'  LIMIT 1",  nodelink->download_database,nodelink->threadinfo->loop_thread,nodelink->size_last, nodelink->md5  , nodelink->threadinfo->myid, nodelink->layer );
	else
		sprintf(sql, "UPDATE `manzhua`.`link_md5`  SET `mylock`='0'     WHERE `link_md5`.`md5` = CAST( 0x%s AS BINARY )   LIMIT 1", nodelink->md5   );
	if (mysql_query (conn, sql))  {
		char message[200];
		sprintf(message,"unlock_link_md5  myid=%d",nodelink->threadinfo->myid);
		write_database_error( conn , message ,sql);
		//mysql_free_result(mysql_store_result(conn));
		return -1;
	}
	//mysql_free_result(mysql_store_result(conn));
	/*
	if(nodelink->web_or_link == IsWeb)
	{
		nodelink->node_web->download = nodelink->download_database;
		//unlock_web_md5 (   nodelink , nodelink->node_web,nodelink->download_database);
	}
	*/


	return 0;


}
 /*
int upgrade_web_layer( struct QNodeLink *nodelink ,int layer)
{
	if( 1 == nodelink->layer )  nodelink->threadinfo->LoopBig.wget_depth++;
	nodelink->layer =  layer;
	nodelink->node_web->layer = 	 layer;

	//ThreadInfo->LoopBig.upgrade_web++;
}
*/
int  lock_link_md5 (MYSQL *conn, struct THREADINFO *ThreadInfo , struct QNodeLink *nodelink)
{  //按条件直接update记录，成功update，即锁定了链接返回1，失败update，那么直接插入数据，插入失败说明有记录，
	//已经被别的线程锁定了，那么返回0，插入成功，说明是新链接，那么返回2；
	//-1 是数据库错误
	//  0 别的线程已经锁定
	//  1 老链接 锁定了
	//  2  新链接锁定

	/*
		1、链接采集的唯一性，A、网址优先，B、深度优先，这样保证一个队列中一个链接只有一次采集机会，减少了重复下载

	*/
		//nodelink->loop = ThreadInfo->nodeWQ->loop;
		struct LINKDATABASE linkdatabase;
 		char sql[500];
		unsigned int	tm;//,lasttm;//,loop;
		//int mylock,layer;
		MYSQL_RES *res;
		MYSQL_ROW row;
		//nodelink->repeat = 0;
		sprintf(sql, "SELECT   UNIX_TIMESTAMP(`tm`) ,`mylock`,`layer`,`download`,`loop`,`web_or_link` ,`size_last` FROM  `manzhua`.`link_md5` WHERE `link_md5`.`md5` = CAST( 0x%s AS BINARY ) LIMIT 1", nodelink->md5 );

		if (mysql_query (conn, sql)) {
			char message[200];
			sprintf(message , "lock_link_md5  myid=%d " , ThreadInfo->myid);
			write_database_error( conn ,message ,sql);
			return -1;
		}  //数据库错误，返回-1
		res = mysql_store_result(conn);
		if(row = mysql_fetch_row(res))
		{

				linkdatabase.tm = 			atoi(row[0]);//strtoul (row[0], NULL, 0);
				linkdatabase.mylock =		atoi(row[1]);//strtoul (row[1], NULL, 0);
				linkdatabase.layer =		atoi(row[2]);// strtoul (row[2], NULL, 0);
				linkdatabase.download =		atoi(row[3]);//strtoul (row[3], NULL, 0);
				linkdatabase.loop  =		atoi(row[4]);//strtoul (row[4], NULL, 0);
				linkdatabase.web_or_link =	atoi(row[5]);//strtoul (row[5], NULL, 0);
				linkdatabase.size_last =	atoi(row[6]);//strtoul (row[6], NULL, 0);
				mysql_free_result(res);res = NULL;

				nodelink->loop_link=  linkdatabase.loop;
				nodelink->download_database = linkdatabase.download; //**********必须赋值，调用的程序要用
				nodelink->size_last = linkdatabase.size_last;

				tm=time((time_t *) NULL);

				//----------------------------------------------------------------------------------------------------
				//库内已经有的采集末级练级，直接放弃,微博的末级链接是不能放弃的
				//----------------------------------------------------------------------------------------------------
				if(0 == nodelink->layer  && IsWeibo != nodelink->node_web->nodeWQ->type)  return update_tm_linkmd5( conn,  nodelink , &linkdatabase  );

				//----------------------------------------------------------------------------------------------------
				//坏链接直接放弃
				//----------------------------------------------------------------------------------------------------
				if(  linkdatabase.download <  Download_Line  )
				{
					if( IsWeb  ==  nodelink->web_or_link  ) nodelink->node_web->download = linkdatabase.download ;//nodelink->node_web->loop_web = nodelink->node_web->nodeWQ->loop_WQ;
					return update_tm_linkmd5( conn,  nodelink , &linkdatabase  );
				}
				//链接已经锁定，强制再锁定这个链接，必须具备几个条件 A新任务比老锁定采集深度更深 B新任务是网址采集CDE

				//---------------------------------------------------------------------------------------------------
				//IsWeb-------------------------------------------------------------------------------------------------
				//----------------------------------------------------------------------------------------------------
				if( IsWeb  ==  nodelink->web_or_link  )
				{
						//更新web_or_link
						if( IsLink   ==  linkdatabase.web_or_link)   // IsWeb + IsLink     网址变化的强制采集一次，以后就不用了
						{
								// IsWeb -> IsLink   都要重新采集，无法确定link是否采集完毕
								//update_link_md5(conn, nodelink->md5, "web_or_link", IsWeb);
								if( nodelink->layer <  linkdatabase.layer)
								{
										nodelink->node_web->layer = 	 linkdatabase.layer;
										nodelink->layer = linkdatabase.layer;
										return lock_linkmd5(conn,nodelink ,IsWeb);
								}
								else if( nodelink->layer ==  linkdatabase.layer)
							 	{
										return lock_linkmd5(conn,nodelink ,IsWeb);
							 	}
								else
								{
										return lock_linkmd5(conn,nodelink ,IsWeb);
								}

						}
						else //  IsWeb + IsWeb    一个服务器采集网址，多个队列在网址入队列时保证了网址的唯一性.队列之间有借鉴用途，比如不通搜索引擎队列采集的末级链接结果是共享的
						{

								if( nodelink->layer <  linkdatabase.layer)
								{
										//upgrade_web_layer( nodelink , linkdatabase.layer);
										nodelink->node_web->layer = 	 linkdatabase.layer;
										nodelink->layer = linkdatabase.layer;
										return lock_linkmd5(conn,nodelink ,IsWeb);
								}
								else if( nodelink->layer ==  linkdatabase.layer) //最正常的网址采集
								{
										if(  ThreadInfo->loop_thread >  linkdatabase.loop   &&  0 == linkdatabase.mylock  ) //
											return lock_linkmd5(conn,nodelink ,IsWeb);

								}
								else
								{
										//update_link_md5(conn, nodelink->md5, "layer", nodelink->layer);
										//if(  ThreadInfo->loop_thread >  linkdatabase.loop   &&  0 == linkdatabase.mylock  )
											return lock_linkmd5(conn,nodelink ,IsWeb);
								}

						}

				}
				//--------------------------------------------------------------------------------------------------
				//isLink-----------------------------------------------------------------------------------------------
				//--------------------------------------------------------------------------------------------------
				else
				{
						if( IsWeb  ==  linkdatabase.web_or_link  ) //link + web
						{
								//更新网址采集深度,更新数据库即可
								if(  nodelink->layer  >  linkdatabase.layer )
								{
									//ThreadInfo->LoopBig.upgrade_web++;
									//return update_link_md5(conn, nodelink->md5, "layer", nodelink->layer);
									return lock_linkmd5(conn,nodelink , linkdatabase.web_or_link);
								}

						}
						else  //link + link  都是链接
						{
								//以库内记录的最大深度采集，这样均衡些
								if(  nodelink->layer <   linkdatabase.layer )
								{

								}
								else if(  nodelink->layer ==  linkdatabase.layer )
								{
									if(ThreadInfo->loop_thread >  linkdatabase.loop   &&  0 == linkdatabase.mylock )
										return lock_linkmd5(conn,nodelink ,nodelink->web_or_link);

								}
								else //必须强采集
								{
									//if(ThreadInfo->loop_thread >  linkdatabase.loop   &&  0 == linkdatabase.mylock )
										return lock_linkmd5(conn,nodelink ,nodelink->web_or_link);
									//else
									//	return update_link_md5(conn, nodelink->md5, "layer", nodelink->layer);
								}

						}
				}
		}
		else
		{
				//新链接
				mysql_free_result(res);res = NULL;
				ThreadInfo->LoopThread.link_parse_new++;
				//nodelink->download_database = Download_OKInit;
				nodelink->loop_link =0;//********************************
				return insert_linkmd5(conn,nodelink->md5, nodelink->threadinfo->myid, nodelink->layer,nodelink->loop_link,nodelink->download_database,nodelink->web_or_link,nodelink->linknew);
		}

		return update_tm_linkmd5( conn,  nodelink , &linkdatabase  );
}



int Downdloadfile(char *Downdloadip , char *filepath ,char *targetfile)
{	//sprintf(buf ,"scp %s%s root@%s:%s/. ;echo $? >%s",tmpdir,_tarfile, remote_ip,remote_dir,sshupdate );
	char buf[200];
	sprintf(buf ,"scp  root@%s:%s  %s ",  Downdloadip,filepath  ,targetfile);
	printf("%s\n",buf);
	system (buf);
}
int read_file_first_line_data(char *file)
{
	char filepath[200];
	sprintf(filepath,"%s/%s",NowWorkingDir,file);
	int data=0;
	FILE   *FILE_web_linkfile;
	FILE_web_linkfile=fopen(filepath,"r");
	if (FILE_web_linkfile == NULL) {  Recorderror(filepath,Errorfile), printf("Searchlinkfile file can not open the file-----file=%s\n",filepath); }
	else{
			while(!feof(FILE_web_linkfile))	//对ls生成的文件中每个文件进行处理
			{

					fscanf(FILE_web_linkfile,	"%d\n",&data);
					//printf("Num_Download_Search = [%d]\n",Num_Download_Search);
					break;
			}
			fclose(FILE_web_linkfile);
	}

	return data;

}
int download_a_file(char *remote_name,int IfDownload  )
{

		int myreturn=0,download_ok;
		char buf[1000],_local_filepath[1000],local_filepath[1000],remoteFilePath[200],order[1000],*p;

		//定义本地文件名
		p = index(remote_name,'/');
		if(p){ //"proxy/2016-11-06_11:11"
				sprintf(local_filepath,"%s/%s",NowWorkingDir,remote_name);
				*p = '\0';
				sprintf(_local_filepath,"%s/%s/_%s",NowWorkingDir,remote_name,p+1);
				*p = '/';
		}
		else{
				sprintf(_local_filepath,"%s/_%s",NowWorkingDir,remote_name);
				sprintf(local_filepath,"%s/%s",NowWorkingDir,remote_name);
		}
		int filesize = (int)(Filesize(local_filepath));
		//printf("------------remote_name=[%s]  size=[%d]\n",remote_name,filesize);
		if(IfDownload > 0  || filesize <=0)
		{
			//定义远程文件名
			sprintf(remoteFilePath,"collector/%s" , remote_name);
			if( strstr(remote_name,"all_source_file.new") ||  strstr(remote_name,"all_source_file_quick")  ||  strstr(remote_name,"all_source_file_no.new") ||   strstr(remote_name,"all_source_file_shield.new")    ){
					sprintf(remoteFilePath,"%s.zip" , remoteFilePath);
					sprintf(local_filepath,"%s.zip",local_filepath);
					sprintf(_local_filepath,"%s.zip",_local_filepath);
					//printf("remoteFilePath[%s]\n_local_filepath[%s]\nlocal_filepath[%s]\n",remoteFilePath,_local_filepath,local_filepath);
			}
			printf("--------[%s]----remote_name=[%s]  size=[%d]\n",Downdloadip,remoteFilePath,filesize);
			download_ok =sftp_file(Downdloadip,"xuning","estar1981xuning64",remoteFilePath,_local_filepath,2,Port);
			if(1 == download_ok  &&  (int)(Filesize(_local_filepath)) >0 ){
					 rename(_local_filepath,local_filepath);
					 printf("%s download ok------------------------\n",remote_name);
					 myreturn =1;
					 if(strstr(local_filepath,".zip")){
							 sprintf(order,"unzip -o  -d %s/  %s",NowWorkingDir ,local_filepath);
							 system(order);
							 printf(" \n" );
					 }
			}
			else{
					printf("%s download fail ????????????????????????????????\n",remote_name );
					myreturn =0;
			}


		}


		return myreturn;


}

int Otherwork(int myid)
{
		return 0;
}

int dosystem(char *buf)
{
		system(buf);
		return 1;
}
int my_fscanf_int(FILE   *fp, int  *data)
{
		char name[1000];
		fscanf(fp,"%s %d\n",&name,data);
		printf("%s--%d\n",name,*data);

}
int my_fscanf_char(FILE   *fp, char   *data)
{
		char name[1000];
		fscanf(fp,"%s %s\n",&name,data);
		printf("%s--%s\n",name,data);

}
int freecfg(char *message,struct MYNUM * Num ,int iffree,struct QNodeWebQueue* nodeWQ)
{

	printf( "freecfg ReadcfgNew is error %s\n" , message);
	Num->WebQueue = 0;
	if(1 == iffree) {free(nodeWQ); nodeWQ = NULL;}

}
char *readinfo(char *begin , char *str ,char *strreturn , struct MYNUM * Num ,int ifprint){
		//读取关键词所在行后边的信息
		char *p,*pp=strreturn;
		*pp = '\0';
		p = strstr(begin, str) ;
		if(p){
				p = p+strlen(str);
				while(*p != '\0'){
						if( !isspace(*p)){
							*pp = *p;
							pp++;
						}
						else if(*p == '\n')
							break;

						p++;
				}
				*pp = '\0';

				if(strlen(strreturn) > 0) {
						printf("%s = [%s]\n",str,strreturn);
						return p;
				}

		}
		if(1 == ifprint) printf("Readcfg is error :%s\n",str);
		//if(nodeWQ && 1 == iffree) free(nodeWQ);
		//Num->WebQueue = 0;

		return NULL;

}



int checkLinkThird(char *link){
	//写新文件链接判断

	/*
	//在提取链接时判断过了
	if(link[linklen-1]=='.' && link[linklen-2]=='z' && link[linklen-3]=='i' && link[linklen-4]== 'p') return 0;
	if(link[linklen-1]=='.' && link[linklen-2]=='r' && link[linklen-3]=='a' && link[linklen-4]== 'r') return 0;
	if(link[linklen-1]=='.' && link[linklen-2]=='d' && link[linklen-3]=='o' && link[linklen-4]== 'c') return 0;
	if(link[linklen-1]=='.' && link[linklen-2]=='e' && link[linklen-3]=='x' && link[linklen-4]== 'e') return 0;
	*/
	//由于微博的兴起，http://t.qq.com/p/t/29236028832053 ，今日头条https://www.toutiao.com/group/6566401284604166669/，这样的信息必须采集，以前只采集.html,htm...等的限制必须取消了
	//|| strstr(link,".htm")  || strstr(link,".shtml")  || strstr(link,".asp")  || strstr(link,".php") || strstr(link,".jsp") )
	if(1 == checkWeb(link , "tieba.baidu.com")  &&  0 == checkWeb(link , "tieba.baidu.com/p/")  )   return 0;
	if(1 == checkWeb(link , "guba.sina.com.cn") && NULL == strstr(link,"s=thread")  )   return 0;
	//if(strstr(link,".cena.com.cn")  && NULL == strstr(link,"content_")  )   return 0;
	//if(strstr(link,".zyctd.com")  && NULL == strstr(link,"article")  )   return 0; //http://www.zyctd.com/article-222599-1.html
	if(1 == checkWeb(link , "t.qq.com")   &&  0 == checkWeb(link , "t.qq.com/p/t/")  )   return 0;
	if(strstr(link,".sogou.") && NULL==strstr(link, ".sogou.com/websearch/art.jsp") )  return 0;
	//if(strstr(link, ".fang.com/hezu/"	) || strstr(link, ".fang.com/chuzu/")  || strstr(link, ".fang.com/house/"))  return 0;
	//if(1 == checkWeb(link , "www.zhihu.com")  && NULL == strstr(link,"/question/") )  return 0;
	//if(strstr(link,".kaixian.tv") && NULL == strstr(link,"/html/") &&  NULL ==  strstr(link,"/gd/")) return 0;

	//判断'/'的次数，少于3个则不要
	int xiegangnum=0,m,linklen = strlen(link);;
	for(m=4 ; m<linklen && xiegangnum<3;m++)
		if(link[m]=='/') xiegangnum++;
	if(xiegangnum<3) return 0;
	//没有数字不是好链接*******************************************************
	if(strcspn(link,"1234567890")<linklen) ;
		else return 0;
	return 1;

}
/*
int Judge_html(char *src)
{
	int i;
	for(i=0;i<KwDeleteHtml.num;i++)
	{
		//if(strstr(src , "http://www.yuleyongpinw.com/pdll.gif")) return 0;
		//printf("%d [%s]\n" , i, KwDeleteHtml.kw_arr[i] );
		if(strstr(src , KwDeleteHtml.kw_arr[i])) return 0;
	}
	return 1;
}
*/
/*
int Judge_Url(char *url)
{
	char *domain;
	int i;
	for(i=0;i<UrlPingBiInEnd.num;i++){
		domain = strstr(UrlPingBiInEnd.kw_arr[i], "://");
		if(domain){
			domain = domain +3;
			if(1 == checkWeb(url , domain))
				return 0;
		}
		else{
			if(strstr(url , UrlPingBiInEnd.kw_arr[i]))
				return 0;
		}
	}
	return 1;

}
*/


/*
const char *webend[]={".com.",".gov.",".net.",".edu.",".org.",".gd.",".com",".gov",".edu", ".org",".cn",".hk",".biz",".cc",".name",".info","tv"};
int webendnum = COUNT(webend);
int return_web(char *link ,char *web)
{

        char *p,*pp ,*begin,webtmp[200];
		int i;
        p = strstr(link,".");
	 if(p==NULL)   return 0;
	 p++;
        if(p==NULL ||  !isalnum (*p) ) return 0;

	  //获取域名
	  p = strstr(link,"http://");
	  if(p == NULL) p = link;
	  else p= p+7;
         pp = strstr(p,"/");
	 if(pp == NULL) {bcopy(p ,webtmp,strlen(p)); webtmp[strlen(p)]='\0';}
	 else  { bcopy(p ,webtmp,pp-p); webtmp[pp-p]='\0';}
	//if(strstr(link,"http://andyjo.blog.sohu.com/")) printf("aaaaaaaaaaa\n");
	 if(strstr(webtmp,"/") || strstr(webtmp,"?")  || strstr(webtmp,"=") ) return 0;

	 for(i=0;i<webendnum;i++)
 	 {
		pp=strstr(webtmp,webend[i] ) ;
		if(pp)
		{
		       begin= webtmp;
			p = pp;
		       while(p>=begin)
	       	{
	       	    p--;
			    if(*p=='.')
				{
				       p++;
				       bcopy(p ,web,pp-p); web[pp-p]='\0';
					return 1;
					break;
				}
	       	}
			break;
		}
 	 }
	//if(strstr(link,"http://andyjo.blog.sohu.com/")) printf("bbbbbb\n");
	 return 0;
}
int return_host(char *link ,char *web)
{
        char *p,*pp  ;

        p = strstr(link,".");
	 if(p==NULL)   return 0;
	 p++;
        if(p==NULL ||  !isalnum (*p) ) return 0;

	  //获取域名
	  p = strstr(link,"http://");
	  if(p == NULL) p = link;
	  else p= p+7;
         pp = strstr(p,"/");
	 if(pp == NULL) {bcopy(p ,web,strlen(p)); web[strlen(p)]='\0';}
	 else  { bcopy(p ,web,pp-p); web[pp-p]='\0';}

	 if(strstr(web,"/") || strstr(web,"?")  || strstr(web,"=") ) return 0;
	 return 1;
}
*/
char * file2strzran( char* file)
{
	/*将文件内容写入字符串,并返回字符串的首地址*/
	/*注意:只用于传文本文件*/

	int fd;
	int fsize; /*file size*/
	struct stat sb;
	char * str = NULL;

	fd = open(file, O_RDONLY);
	if(-1 == fd)
		{close(fd);return NULL;}

	fstat(fd, &sb);
	fsize = sb.st_size;
	if(fsize > MaxWebSize)  {close(fd);return NULL;}

				/*获得文件大小*/
	str =(char *) calloc(sizeof(char), fsize + 1);

	//str = (char *)malloc(sizeof(char)*(fsize + 1));  //zran
				/*为str分配空间*/
	if(fsize != read(fd, str, fsize))
		{close(fd);return NULL;}

	close(fd);

	return str;
}

int getalivewebnum(QListWeb *QL)
{
	int lastwebnum=0;
	QNodeWeb *p;
	p=QL->front;
	while(p   )
	{
		if( p->download > 0) //&& p->webinfo.loop< loop  p->webinfo.mylock< 1 &&
			lastwebnum++;
		p =p->next;
	}
	return lastwebnum;
}


int  FirstWork(int old_myid  )
{	//线程调度程序，控制整个采集开始与结束

  	unsigned  int now_tm  ;
	char buf[200],sql[1000] ;
	char nowtime_str[200];

	Server.EnforceLinkLayerNum = 0;
	Server.RepeatDownloadLinkLayerNum  = 0;
	Server.DownloadError = 0;

	Server.badlinknum=0;
	Server.MiddleLoopBeginTime = time((time_t *) NULL);
	//Server.MiddleLoop = 1;
	int aaaaaaaaaaa=1;
	int lastwebnum=0;



	unsigned int  FirstWorkBeginTime = time((time_t *) NULL);
	IfOut = 0;
	int smallloop = 0;
	unsigned int last_chrome_tm = time((time_t *) NULL);

      while(1) //middle
      	{
		now_tm =time((time_t *) NULL);

		Mytime(nowtime_str);
		if(smallloop > 0) {
			//TotalQLWebQueue( QLWebAll  );
		}
		/*
		//每4小时
		if(now_tm -last_chrome_tm > 3600*4){
			kill_process("chrome");
			last_chrome_tm = now_tm;
		}
		*/
		if(now_tm-FirstWorkBeginTime  > BigLoopIntervalTime && strstr(nowtime_str,RebootTime)   )	//*24  60*  &&    1 == getwebloop(QLWeb[isQLWeb])  strstr(nowtime_str," 01:")
		{
			break;
		}


		sleep(600);
		smallloop++;

      	}
	IfOut=1;

	sprintf(buf,"%d   i am afterwork end............................FirstWork\n"  ,old_myid );
	printf("%s\n",buf);
	Recordwork(buf,Recordworkfile);
 	//mysql_close(conn);

	return 0;

}





/*
void websort(struct LINKINFO stu[],int count)
{  //采集层数递减排序
      int i,j;
      struct LINKINFO temp;
      for(i=0;i<count-1;i++)
      {
          for(j=0;j<count-1-i;j++)
          {
               if(stu[j+1].layer>stu[j].layer)
               {
                     temp=stu[j+1];
                     stu[j+1]=stu[j];
                     stu[j]=temp;
               }
          }
      }
}
*/
void InitQLWeb(QListWeb* QL)
{
    if(QL==NULL)
        QL=(QListWeb*)malloc(sizeof(QListWeb));
    QL->front=NULL;
    QL->end=NULL;
}
void mallocQLWeb(struct QNodeWebQueue* node , int alllinklen)
{
	char message[100];

	//alllinklen
	node->QLWebPub_buf = (char *)malloc(alllinklen);
	if(node->QLWebPub_buf)
	{
		memset (node->QLWebPub_buf,'\0',sizeof(node->QLWebPub_buf));
		node->QLWebPub_link_p = node->QLWebPub_buf;
	}
	else
	{
		sprintf(message ,"mallocQLWeb error alllinklen = %d",alllinklen);
		RecordMessage(message ,Errorfile,1);

	}
/*
	//allweblen
	node->QLWebPub_web= (char *)malloc(allweblen);
	if(node->QLWebPub_web)
	{
		memset (node->QLWebPub_web,'\0',sizeof(node->QLWebPub_web));
		node->QLWebPub_web_p = node->QLWebPub_web;
	}
	else
	{
		sprintf(message ,"mallocQLWeb error allweblen = %d",allweblen);
		RecordMessage(message ,Errorfile,1);
	}
*/
}
/*
void mallocQLWeb_all(struct QNodeWebQueue* nodeWQ  ,struct WEBINFOBASE *webinfo)
{
		 int alllinklen,int allweblen
		char nowkw[500],link_tmp[500],*p;
		p = strstr(nodeWQ->link,"estarsearch");//  %E5%98%89%E9%87%8C

		strncpy(link_tmp,nodeWQ->link ,p - nodeWQ->link);
		link_tmp[p - nodeWQ->link] = '\0';



		FILE * FILE_linkfile;
		int i=0;

		this_server_CaijiMore_num = 0;
		FILE_linkfile=fopen(nodeWQ->FileKw,"r");
		if (FILE_linkfile == NULL) perror ("Error opening file");
		else
		{
			while ( ! feof (FILE_linkfile) )
			{
				if ( fgets (nowkw , 1024 , FILE_linkfile) != NULL )
				{
					if(strlen(nowkw) > 400) continue;
					sprintf(webinfo->link ,"%s%s" , link_tmp ,nowkw   );
					Del_other(webinfo->link );
					alllinklen = alllinklen +  strlen(webinfo->link )+1;
					allweblen = allweblen +  strlen(webinfo->web)+1;
				}
			}
			fclose (FILE_linkfile);

		}

		mallocQLWeb(nodeWQ ,alllinklen , allweblen);


}
*/
/*
init_loop_nodeWQ(struct QNodeWebQueue* nodeWQ)
{
	//nodeWQ->num_sh_public = 0;
	nodeWQ->loop_begin_tm = time((time_t *) NULL);
	//nodeWQ->loop_num_done = 0;
}
*/
unsigned  int  CountQLWeb(QListWeb* QL)
{	//遍历显示链表所有单元
       unsigned  int i=0;
	if(QL)
	{
		    QNodeWeb*p;
		    p=QL->front;
		    while(p   )
		    {
		        //printf("%d\t",p->link);
		        i++;
		        p=p->next;
		    }
	}
      return i;
}
int InitQLWebAll( struct QNodeWebQueue* node   ,struct MYNUM * Num,struct CONFIGSET *config,  struct WEBINFOBASE *webinfo)
{

	sprintf(node->link,"%s",webinfo->link);
	sprintf(node->web,"%s",webinfo->web);
	node->webid_pub =webinfo->webid;
	 int num_thread;
	 node->always_download = 0;//默认都不下载
	switch(config->type)
	{
		case IsWeb:
					num_thread = config->num_thread;
					Num->thread_web = Num->thread_web + num_thread;
					break;
		case IsSearch:
					num_thread = 1;
					Num->thread_search = Num->thread_search+ num_thread;
					break;
		case IsWeibo:
					if(strstr(node->link,"s.weibo.com")){
						num_thread = config->num_thread;
						Num->thread_weibo= Num->thread_weibo+ num_thread;
					}
					else{
						num_thread = 1;
						Num->thread_weibo_search= Num->thread_weibo_search+ num_thread;
					}

					break;
		case IsWeiXin:
					num_thread = config->num_thread;
					Num->thread_weixin= Num->thread_weixin+ num_thread;
					break;
		default://处理非
				printf("dddddddddddddddddddd333333ddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd\n");
				break;

	}
	node->num_thread = num_thread;//采集的线程数量
	node->type = config->type;   //队列的类型网站、搜索引擎，基本就这2种类型 IsWeb  IsSearch   //0是网站，1是微博，2是搜索引擎采集网址 , 100是网址
	node->Tools = config->Tools;  //链接方式
	node->Connection = config->Connection;  //链接方式
	node->IfDownload = config->IfDownload;  //是否下载网址和关键词文件
	strcpy(node->webServer , config->webServer);//web服务地址

	sprintf(node->FileWeb ,"%s" ,config->FileWeb ); //网址文件
	sprintf(node->FileKw ,"%s" ,webinfo->FileKw );//关键词文件
	if( config->type != IsWeb ) download_a_file(node->FileKw,node->IfDownload  );

	node->ServerNum = config->ServerNum; //几个服务器参与采集
	node->ServerOrder = config->ServerOrder; //参与采集服务器中排序号
	node->NumSHInThread = config->NumSHInThread; //一个线程中sh文件个数，也是ThreadWgetMaxnum
	node->NumWgetInSH = config->NumWgetInSH;     //sh文章中wget数量MaxwgetnumInSh
	node->IntervalTimeWeb = config->IntervalTimeWeb;  //同一个网址采集间隔
	node->WgetTimeOut = config->WgetTimeOut;  //wget超时时间
	node->NumDownloadError  = 0;

	//QLWebAll->type = type;
	//QLWebAll->tinytype = tinytype;
	//QLWebAll->myid_begin = myid_begin;
	//QLWebAll->num_thread= num_thread;


	node->QLWeb= (QListWeb*)malloc(sizeof(QListWeb));
	InitQLWeb(node->QLWeb);   //初始化这个队列

	node->QLWebPub_buf = NULL;
	node->QLWebPub_link_p = NULL;
	//node->QLWebPub_web = NULL;
	//node->QLWebPub_web_p = NULL;


	//node->QLThread= (QListThread*)malloc(sizeof(QListThread));
	//InitQLThread(node->QLThread);   //初始化这个队列

	//node->QLWgetWaiting=(struct QList*)malloc(sizeof(struct QList));
	//InitQL(node->QLWgetWaiting);   //初始化这个队列

	//------------------------------------------------------------------
	node->threadsNum = 0;
	node->threads = NULL;


	node->myid_begin = Num->thread_download_index;
	node->num_thread= num_thread;

	node->num_web =0;
	node->num_web_valid=0;
	node->num_web_working=0;
	node->index = Num->WebQueue;


	if(BigLoop==1)
		node->loop_WQ = 0;
	else
		node->loop_WQ = 1;//否则会空转一圈
	node->loop_thread_max = 1;

	//node->QLWgetWaiting= (struct QList*)malloc(sizeof(struct QList));
	//InitQL(node->QLWgetWaiting);   //初始化这个队列

	//init_loop_nodeWQ(node);
	/*
	node->loop_begin_tm = time((time_t *) NULL);
	node->loop_num_done = 0;
	node->num_sh_public=0;
	*/

	if(Connection_proxy_all == node->Connection  ||Connection_proxy_web == node->Connection){
		node->index_proxy = Num->goodproxy;
		Num->goodproxy++;

	}else{
		node->index_proxy = NotUseProxy;
	}
	/*
	if(IsWeb == node->type || IsWeiXin== node->type)
	{
		node->index_proxy = NotUseProxy;
	}
	else
	{
		node->index_proxy = Num->goodproxy;
		Num->goodproxy++;
	}
	*/

	Num->thread_download_index = Num->thread_download_index +node->num_thread;
	Num->WebQueue++;
	Num->thread_all = Num->thread_all + node->num_thread;
	Num->wget = Num->wget + node->num_thread * node->NumSHInThread;



	return 0;
}
/*
int count_space_by_kw(struct QNodeWebQueue* node ,char *kwfile, struct WEBINFOBASE *webinfo,char *str_replace ,int index_proxy)
{
		printf("[%s]\n" , kwfile);
		int alllinklen=0;
		int allweblen=0;
		FILE * FILE_kw;
	 	char  nowkw[1024];
		int i=0;
		char linknew[1024],*p,*pp,c;

		//p = strstr(webinfo->link,str_replace);
		////pp= p+strlen(str_replace);
		//c = *p;
		//*p = '\0';

		FILE_kw=fopen(kwfile,"r");
		if (FILE_kw == NULL)
			perror ("Error opening file");
		else{
			while ( ! feof (FILE_kw) ){
				if ( fgets (nowkw  , 1024 , FILE_kw) != NULL ){
					//sprintf(linknew ,"%s%s%s",webinfo->link,nowkw,pp);//2014
					Del_other(nowkw);
					alllinklen = alllinklen +  strlen(nowkw)+2;//+1;
					//allweblen = allweblen +  strlen(webinfo->web)+1;
					i++;
				}
			}
			fclose (FILE_kw);
		}
		printf("%s alllinklen = [%d] allweblen = [%d]\n",webinfo->web,alllinklen , allweblen);
 		mallocQLWeb(node ,alllinklen );
		sprintf(node->link,"%s",webinfo->link);
		sprintf(node->web,"%s",webinfo->web);
		node->index_proxy = index_proxy;
		//*p = c;


}
*/
int RecordMessage(char *message,char *filename,int ifprintf)
{
	//记录信息
	char nowtime[20];
	FILE   *fp;

	fp=fopen(filename,"a+");
	if(fp==NULL)
	{
		printf("RecordMessage can not open the file :%s\n",filename);
		return 0 ;
	}
	Mytime(nowtime);
	fprintf(fp, "%s---%s\n", nowtime, message);
	fclose(fp);

	if(1==ifprintf) printf("%s\n" , message);
    	return 1;
}
int readweb(QNodeWebQueue *nodeWQ){

			FILE * FILE_web_linkfile;
			int i , line,len,alllinklen=0,allweblen=0;
			int this_server_web_begin,this_server_web_end;
			char *p,md5[100],message[200],tmp[100];
			struct WEBINFOBASE webinfo;

			FILE_web_linkfile=fopen(nodeWQ->FileWeb,"r");
			if (FILE_web_linkfile == NULL) {
				Recorderror(nodeWQ->FileWeb,Errorfile), printf("Weblinkfile file can not open the file-----file=%s\n",nodeWQ->FileWeb);
				return 0;
			}
			else{

					i=0; line=-1;
					while(!feof(FILE_web_linkfile)){ 	//对ls生成的文件中每个文件进行处理

							//http://www.cq.chinanews.com.cn		  1 	   12965	   0
							if(line<0)  {
							    fscanf(FILE_web_linkfile,	"%d\n",& Server.allwebnum);
							    printf("readweb type=%d    Server.allwebnum= [%d]\n",nodeWQ->type, Server.allwebnum);
							    nodeWQ->num_web= (int)( Server.allwebnum/nodeWQ->ServerNum )+1;


							    if(nodeWQ->num_web> Server.allwebnum)
									nodeWQ->num_web= Server.allwebnum;
							    this_server_web_begin = nodeWQ->ServerOrder*nodeWQ->num_web;
							    this_server_web_end =   this_server_web_begin + nodeWQ->num_web;
							    if(this_server_web_end>=Server.allwebnum)
									this_server_web_end=Server.allwebnum-1;
							}
							else{
								if(strstr(nodeWQ->FileWeb,".25"))
									fscanf(FILE_web_linkfile,	"%s %d %d %s %s\n",webinfo.link,&webinfo.layer,&webinfo.webid,webinfo.web,webinfo.ifout);
								else{
									fscanf(FILE_web_linkfile,	"%s %d %d %s\n",webinfo.link,&webinfo.layer,&webinfo.webid,webinfo.web);
									sprintf(webinfo.ifout , "in");
								}

								if(  line>=this_server_web_begin  &&   line<=this_server_web_end)  {
									//printf("%s %d %u [%s][%s]\n",  webinfo.link , webinfo.layer, webinfo.webid, webinfo.web,webinfo.ifout);
									//sprintf(webinfo.link,"%s",link);
									if(strstr(webinfo.link,"javascript") != NULL  )
										continue;
									len =strlen(webinfo.link);
									if(checkLinkFirst(webinfo.link, len)<1)
										continue;
									//如果是没有目录的网址，如http://www.sina.com.cn/ 去掉尾部'/'(而不是http://www.sina.com.cn/news/)
									p = strstr(webinfo.link,"://");
									if(p){
										p = p +3;
										p = index(p , '/') ;
										if(p != NULL && *(p+1) == '\0'){
											webinfo.link[len-1] ='\0';
										}
									}


									Del_other(webinfo.link);
									convert_unicode(webinfo.link);
									alllinklen = alllinklen +  strlen(webinfo.link)+2;//原来是1，但会内存错误

									//if(1== getDomain( webinfo.link ,domain ))
									//	sprintf(webinfo.web,"%s" ,domain);
									//allweblen = allweblen +  strlen(webinfo.web)+2;
									i++;

								}
							}
							line++;		//if(line > 62000) break;
					}
					fclose(FILE_web_linkfile);

			}
			//printf("web alllinklen = [%d] allweblen = [%d]\n",alllinklen , allweblen);
			mallocQLWeb(nodeWQ ,alllinklen );
			nodeWQ->link[0] = '\0';
			nodeWQ->web[0] = '\0';
			//nodeWQ->index_proxy = -1;

			sprintf(message,"web alllinklen = [%d] allweblen = [%d]",alllinklen , allweblen);
			RecordMessage(message,Recordworkfile,1);
			//------------------------------------------------------------------------------------------
			//读采集网址
			//------------------------------------------------------------------------------------------
			struct LINKDATABASE linkdatabase;
			int download,loop;
			nodeWQ->num_web = 0;
			FILE_web_linkfile=fopen(nodeWQ->FileWeb,"r");
			if (FILE_web_linkfile == NULL) {
				//Recorderror(nodeWQ->FileWeb,Errorfile), printf("Weblinkfile file can not open the file-----file=%s\n",nodeWQ->FileWeb);
				sprintf(message , "Weblinkfile file can not open the file-----file=%s" ,nodeWQ->FileWeb);
				RecordMessage(message,Errorfile,1);
				return 0;
			}
			else{

					MYSQL *conn;
					conn = mysql_conn_init("manzhua");
					if(!conn) {
						RecordMessage("can not open dababase:manzhua" ,Errorfile,1);
						return 0;
					}


					int new_or_old;
					i=0; line=-1;
					while(!feof(FILE_web_linkfile)){ 	//对ls生成的文件中每个文件进行处理

							//http://www.cq.chinanews.com.cn		  1 	   12965	   0
							if(line<0)  {
							      fscanf(FILE_web_linkfile,	"%d\n",&Server.allwebnum);
							}
							else{
								if(strstr(nodeWQ->FileWeb,".25"))
									fscanf(FILE_web_linkfile,	"%s %d %d %s %s\n",webinfo.link,&webinfo.layer,&webinfo.webid,webinfo.web,webinfo.ifout);
								else{
									fscanf(FILE_web_linkfile,	"%s %d %d %s\n",webinfo.link,&webinfo.layer,&webinfo.webid,webinfo.web);
									sprintf(webinfo.ifout , "in");
								}
								if(  line>=this_server_web_begin  &&   line<=this_server_web_end)   {
									if(strstr(webinfo.link,"javascript") != NULL  )
										continue;

									//1 、 简写网址变换标准网址 http://sina.com.cn	  => http://www.sina.com.cn
									char domain[100],host[200];
									if(1 == getDomain(	webinfo.link , domain)){
										if(1 == getHost(webinfo.link , host)){
											if(0 == strcmp(domain,host) ){
												//printf("InsertQLWeb  [%s]\n" , webinfo->link );
												ReplaceStr(webinfo.link , "://","://www.");
												//printf("InsertQLWeb  [%s]\n\n" , webinfo->link );
											}

										}
									}
									//2、 如果是没有目录的网址，如http://www.sina.com.cn/ 去掉尾部'/'(而不是http://www.sina.com.cn/news/)
									p = strstr(webinfo.link,"://");
									if(p){
										p = p +3;
										p = index(p , '/') ;
										if(p != NULL && *(p+1) == '\0'){
											len =strlen(webinfo.link);
											webinfo.link[len-1] ='\0';
										}
									}


									len =strlen(webinfo.link);
									if(checkLinkFirst(webinfo.link, len)<1) {
										printf("readweb error [%s] [%s]\n" ,nodeWQ->FileWeb, webinfo.link);
										continue;
									}



									Del_other(webinfo.link);
									convert_unicode(webinfo.link);
									md5_gen_link(md5, webinfo.link);

									//if(HAVE == SearchQLShieldWeb_by_database(conn, webinfo.link))
									//	continue;

									struct QNodeShieldWeb *domainNode =NULL;
									if(1== getDomain( webinfo.link ,webinfo.domain )){
										//******************************************************************************************
										//首先要查询数据库,如果这个链接的主域或二级域名已经被屏蔽了，那么就放弃这个链接
										//******************************************************************************************

										char md5_domain[100];
										md5_gen(md5_domain, webinfo.domain);
										if(domainOnly  ==  query_md5_web_md5_no (conn,md5_domain) )
											continue;

										//查询主域是否在屏蔽动态数组中，在，返回地址建立关联，不在，返回NULL
										 domainNode = QLShield_Domain_Search( QLShieldWeb , webinfo.domain);
									}else{
										printf("[%s]\n" , webinfo.link);
										//sleep(10000);
										continue;
									}


									//int loop = have_link_md5(conn, md5,BigLoop) ;

									if(webinfo.layer < PubLayer)
										webinfo.layer = PubLayer; //公共采集深度，定义了这个服务器所有的采集深度

									if(strstr(webinfo.link,"estar_")) {
									 	webinfo.tinytype= IsReplaceWeb;
										download = Download_OKForever;
									}
									else {
									 	webinfo.tinytype= IsNormal;
										download = Download_OKInit;
									}

									if(1 == read_database_info(conn,md5, &linkdatabase ) ) {//老网址
										//更新深度
										if(webinfo.layer > linkdatabase.layer ) {
											linkdatabase.layer = webinfo.layer;
											update_link_md5(conn, md5, "layer",  linkdatabase.layer);
											//是否要更新一下loop，避免采集老文章
											update_link_md5(conn, md5, "loop", 0);
										}

										//更新类型
										if(IsLink == linkdatabase.web_or_link )
											update_link_md5(conn, md5, "web_or_link",  IsWeb);
										else //是不同队列之间重复的网址，必须放弃
											continue;

										new_or_old = 0;

									}
									else{  //新网址
										linkdatabase.tm = 0;
										linkdatabase.mylock =	0;
										linkdatabase.layer =	 webinfo.layer;
										linkdatabase.download = download;
										linkdatabase.loop  = 0;
										linkdatabase.web_or_link  = IsWeb;
										new_or_old = 1;
									}
									nodeWQ->num_web = nodeWQ->num_web + InsertQLWeb( conn,nodeWQ ,  &webinfo  ,&linkdatabase,new_or_old ,domainNode);

									i++;
								}
							}
							line++;
					}
					fclose(FILE_web_linkfile);
					mysql_close(conn);

					sprintf(message ,"this_server_web_num = [%d]  CountQLWeb=%d\n",nodeWQ->num_web,CountQLWeb(nodeWQ->QLWeb));
					RecordMessage(message,Recordworkfile,1);

					//printf("this_server_web_num = [%d]  CountQLWeb=%d\n",nodeWQ->num_web,CountQLWeb(nodeWQ->QLWeb));
					IndexQLWeb(  nodeWQ->QLWeb);
			}

			//------------------------------------------------------------------------------------------
			//index
			//------------------------------------------------------------------------------------------



}
int get_kw_replace(char *link,char *kw_replace){
	char *p = strstr(link ,"estar") ,*pp = kw_replace;
	if(p){
		while(isalpha(*p)){
			*pp = *p;
			p++;
			pp++;
		}
		*pp = '\0';
	}
	else{
		printf("get_kw_replace eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee\n");
	}
}
int readweb_by_kw(QNodeWebQueue *nodeWQ){
		printf("[-------------%s]\n",nodeWQ->link);
		int alllinklen=0, allweblen=10;
		char link_tmp[500],*p;
		//p = strstr(nodeWQ->link,"estarsearch");//  %E5%98%89%E9%87%8C
		//*p = '\0';
		get_kw_replace(nodeWQ->link,nodeWQ->kw_replace);
		printf("[%s]\n",nodeWQ->kw_replace);
		struct WEBINFOBASE webinfo;
		FILE * FILE_FileKw;
		int i=0;


		FILE_FileKw=fopen(nodeWQ->FileKw,"r");
		if (FILE_FileKw == NULL) perror ("Error opening file");
		else
		{
			while ( ! feof (FILE_FileKw) )
			{
				if ( fgets (webinfo.kw , 1024 , FILE_FileKw) != NULL )
				{
					if(strlen(webinfo.kw) > 400) continue;
					//sprintf(webinfo.link ,"%s%s" , link_tmp ,nowkw   );
					Del_other(webinfo.kw );
					if(0 == strlen(webinfo.kw) ) continue;
					alllinklen = alllinklen +  strlen(webinfo.kw )+2;//+1;
					//allweblen = allweblen +  strlen(nodeWQ->web)+1;
				}
			}
			fclose (FILE_FileKw);
		}

		mallocQLWeb(nodeWQ ,alllinklen );


		//------------------------------------------------------------------------------------------
		//读采集网址
		//------------------------------------------------------------------------------------------
		int new_or_old;
		FILE_FileKw=fopen(nodeWQ->FileKw,"r");
		if (FILE_FileKw == NULL) perror ("Error opening file");
		else
		{
			struct LINKDATABASE linkdatabase;
			MYSQL *conn;
			conn = mysql_conn_init("manzhua");
			if(!conn)
			{
				printf ("数据库无法打开\n");
				return 0;
			}

			//找domainNode地址
			struct QNodeShieldWeb *domainNode =NULL;

			if(1== getDomain(nodeWQ->link ,webinfo.domain )){
				//sprintf(webinfo.web,"%s" ,domain);
				//插入一个节点，并且domain赋值
				 //domainNode = QLShield_Domain_Insert( QLShieldWeb ,webinfo.domain);
				 domainNode = QLShield_Domain_Search( QLShieldWeb ,webinfo.domain);
			}else{
				printf("[%s]\n" , webinfo.link);
				sleep(10000);
			}
			sprintf(webinfo.web,"out");
			int num = -1;
			char md5[100];
			while ( ! feof (FILE_FileKw) ){
				num++;



				if ( fgets (webinfo.kw , 1024 , FILE_FileKw) != NULL )
				{
					if(nodeWQ->ServerOrder	!= num % nodeWQ->ServerNum)   continue; //20180718 ,关键词队列，拆分，按照余数对应ServerOrder原则

					if(strlen(webinfo.kw) > 400) continue;
					Del_other(webinfo.kw );
					if(0 == strlen(webinfo.kw) ) continue;
					sprintf(webinfo.link ,"%s%s" , nodeWQ->link ,webinfo.kw );

					md5_gen_link(md5, webinfo.link);

					if(IsWeibo== nodeWQ->type)
						webinfo.layer = 0;
					else
						webinfo.layer = 1;

					webinfo.tinytype =IsNormal;

					if(  1 == read_database_info(conn,md5, &linkdatabase ) ) //老网址
					{
						//更新深度
						if(webinfo.layer > linkdatabase.layer )
						{
							linkdatabase.layer = webinfo.layer;
							update_link_md5(conn, md5, "layer",  linkdatabase.layer);
							//是否要更新一下loop，避免采集老文章
							//update_link_md5(conn, md5, "loop", 0);
						}

						//更新类型
						if(IsLink == linkdatabase.web_or_link )
						{
							update_link_md5(conn, md5, "web_or_link",  IsWeb);
						}
						else
						{
							//是不同队列之间重复的网址，必须放弃
							continue;
						}
						new_or_old =0;

					}
					else  //新网址
					{
						linkdatabase.tm = 0;
						linkdatabase.mylock =	0;
						linkdatabase.layer =	 webinfo.layer;
						linkdatabase.download = Download_OKForever;
						//if(IsWeiXin== nodeWQ->type)
						//	linkdatabase.loop  = 1;
						//else
							linkdatabase.loop  = 0;
						linkdatabase.web_or_link  = IsWeb;
						new_or_old = 1;
					}
					webinfo.webid = nodeWQ->webid_pub;
					// printf("[%d][%s]\n" ,webinfo.webid,webinfo.link );
					sprintf(webinfo.ifout,"out");

					InsertQLWeb( conn,nodeWQ ,  &webinfo  ,&linkdatabase,new_or_old , domainNode);
					nodeWQ->num_web++;

					i++;

				}
			}
			fclose (FILE_FileKw);
			mysql_close(conn);
			printf("this_server_web_num = [%d]  CountQLWeb=%d\n",nodeWQ->num_web,CountQLWeb(nodeWQ->QLWeb));
			IndexQLWeb(  nodeWQ->QLWeb);
		}




}
int do_base_work(struct QListWebQueue* QLWebAll ,  struct MYNUM * Num)
{
	char  buf[1000];
	int filesize,now_tm;
	//获取当前目录
	getcwd(NowWorkingDir,sizeof(NowWorkingDir));
	printf("NowWorkingDir : [%s]\n" ,  NowWorkingDir);

	//先删除那些.sh进程
	kill_process("_S_task_");
	//kill_process("manzhuasavedir");//??????
	kill_process("estarmanzhuawget");//????
	//kill_process("chrome");
	kill_process("phantomjs");

	//时间同步 http://www.cnblogs.com/weaver1/archive/2012/03/15/2397491.html
	//dosystem("/usr/sbin/ntpdate ntp.api.bz");
	dosystem("/usr/sbin/ntpdate us.pool.ntp.org");
	dosystem("rdate -s time.nist.gov");

	//删除数据库错误记录文件
	sprintf( buf,"rm  %s -rf", ErrorFile);
	dosystem(buf);
	//删除错误记录文件
	//dosystem("rm  /estar/myerror/* -rf");

	/*
	sprintf( buf,"rm  %s -rf", Encadir);
	system(buf);
	mkdir(Encadir,0755);
	*/
        //给编码转换的程序数组赋值
	sprintf( Fcharset[0].keyword,"UTF-8");
	sprintf( Fcharset[1].keyword,"big5");
	sprintf( Fcharset[2].keyword,"utf-8");
	sprintf( Fcharset[3].keyword,"BIG5");
	sprintf( Fcharset[4].keyword,"Big5");
	sprintf( Fcharset[5].keyword,"Utf-8");
	//Downdload_conf_file();


	/*
	mkdir("/estar/webhashfile/",0755);
	mkdir("/estar/myerror/",0755);
	mkdir("/estar/newhuicong2/",0755);
	mkdir("/estar/newhuike2/",0755);
	mkdir("/estar/record/",0755);
	mkdir("/estar/repeat/",0755);
	mkdir("/estar/repeattmp/",0755);
	mkdir("/estar/tmp/",0755);
	mkdir("/estar/ups/",0755);
	*/


	//看看记录文件,如果记录文件大于1M，那么另外开一个文件
	/*
	now_tm=time((time_t *) NULL);
	filesize=Filesize(Recordworkfile);
	if(filesize>1000000)
	{
		sprintf(buf,"%s.%d",Recordworkfile,now_tm);
		rename(Recordworkfile,buf);
	}
	*/
	ArrangeLogFile(Recordworkfile,  1000000 ,   5);

}
/********************************************************************************************
* 读多个搜索队列文件和关键词
* 1、weixin_search.new
* 2、weibo_search.new
* 3、all_source_file_search.new
每个文件里有1个或多个搜索连接，并且指定了配置的关键词文件
********************************************************************************************/
struct QNodeWebQueue*  InsertQLWebQueue_many(struct QListWebQueue* QLWebAll,struct CONFIGSET *config,   struct MYNUM * Num)
{

			FILE * FILE_web_linkfile=fopen(config->FileWeb ,"r");
			if (FILE_web_linkfile == NULL) {  Recorderror(config->FileWeb,Errorfile), printf("Weblinkfile file can not open the file-----file=%s\n",config->FileWeb); }
			else
			{
					struct WEBINFOBASE webinfo;
					char *p ;
					int line=-1,m =0,len ;
					while(!feof(FILE_web_linkfile))	//对ls生成的文件中每个文件进行处理
					{
							//http://www.cq.chinanews.com.cn		  1 	   12965	   0
							if(line<0)
							{
							    fscanf(FILE_web_linkfile,	"%d\n",&this_server_CaijiMore_num);
							    printf("this_server_CaijiMore_num = [%d]\n",this_server_CaijiMore_num);
							}
							else
							{
									fscanf(FILE_web_linkfile,	"%s %d %d %s %s\n", &webinfo.link ,&webinfo.layer,&webinfo.webid, &webinfo.web, &webinfo.FileKw);


									//sprintf(webinfo.link,"%s",link);
									if(strstr(webinfo.link,"javascript") != NULL  ) continue;
									len =strlen(webinfo.link);
									if(checkLinkFirst(webinfo.link, len)<1) continue;
									p = webinfo.link;
									p = p +7;
									p = index(p , '/') ;
									if(p != NULL && *(p+1) == '\0')
									{
										webinfo.link[len-1] ='\0';
									}
									Del_other(webinfo.link);
									convert_unicode(webinfo.link);
									Del_other(webinfo.FileKw);
									printf("[%d][%s]\n" ,webinfo.webid,webinfo.link );

									//-------------------------------------------------------------------------
									//生成队列节点----------------------------------------------------------------
									//-------------------------------------------------------------------------
									QNodeWebQueue* nodeWQ= InsertQLWebQueue( QLWebAll , config,     Num  ,&webinfo);
									readweb_by_kw(nodeWQ);
									//printf("Num_Download_Search=[%s]    QLWebAll[order].index_proxy=%d\n",  nodeWQ->index_proxy);
								      m++;

							}
							line++;
					}
					fclose(FILE_web_linkfile);

			}




}
int create_nodeWQ(struct QListWebQueue* QLWebAll,struct CONFIGSET *config,   struct MYNUM * Num)
{
		struct QNodeWebQueue* nodeWQ;
		if(IsWeb == config->type)
		{
			struct WEBINFOBASE webinfo;
			webinfo.link[0] = '\0';
			webinfo.web[0] = '\0';
			webinfo.FileKw[0] = '\0';
			nodeWQ= InsertQLWebQueue( QLWebAll ,config,Num, &webinfo );


			//建立web节点队列
			readweb(nodeWQ);
		}
		//建立多个队列 ，主要搜索引擎，微信搜索，微博搜索等
		else{
			//建立多个队列节点,返回第一个节点
			 nodeWQ= InsertQLWebQueue_many(QLWebAll, config,Num );

			//为每个节点计算分配空间

			//为每个节点中的web队列赋值


		}
}

#include <iconv.h>
/*代码转换:从一种编码转为另一种编码*/
int code_convert(char *from_charset,char *to_charset,char *inbuf,size_t inlen,char *outbuf,size_t outlen)
{
	iconv_t cd;
	int rc;
	char **pin = &inbuf;
	char **pout = &outbuf;
	cd = iconv_open(to_charset,from_charset);
	if (cd==0)
	{
		iconv_close(cd);
		return -1;
	}
	memset(outbuf,0,outlen);
	if (iconv(cd,pin,&inlen,pout,&outlen)==-1)
	{
		iconv_close(cd);
		return -1;
	}
	iconv_close(cd);
	return 0;
}
/*UNICODE码转为GB2312码*/
int u2g(char *inbuf,size_t inlen,char *outbuf,size_t outlen)
{
	return code_convert("utf-8","GB18030",inbuf,inlen,outbuf,outlen);//"宏碁" GB18030   GBK  http://www.efeedlink.com.cn/info/details-6097654abb51252a90.html
}
/*GB2312码转为UNICODE码*/
int g2u(char *inbuf,size_t inlen,char *outbuf,size_t outlen)
{
	return code_convert("GBK","utf-8",inbuf,inlen,outbuf,outlen);
}

int g2utf8(char *inbuf,size_t inlen,char *outbuf,size_t outlen)
{
	return code_convert("gb2312","utf-8",inbuf,inlen,outbuf,outlen);
}


int utf8_to_gb(char *gbstr, char *tmp)
{
		int rec = u2g(gbstr,strlen(gbstr),tmp,strlen(gbstr)+1);

		// m_iconv("utf-8","GB18030", gbstr, strlen(gbstr), tmp, strlen(gbstr)+1);
		return rec;
}

int gb_to_utf8(char *gb , char *tmp)
{

	int rec = g2u(gb,strlen(gb),tmp,strlen(gb)*2);
	//printf("#####  %d\n",rec);
	//sprintf(str,"%s",tmp );

}
int big5_to_utf8(char *big5 , char *tmp)
{

	return code_convert("BIG5","utf-8",big5,strlen(big5),tmp,strlen(big5)*2);

}
/*
int read_file_kw(struct KWDELETEHTML *KwDeleteHtml)//char *filename ,char **str_arr)
{

		printf("[read_file_kw-------------read_file_kw]\n") ;

		char str_tmp[500],str_tmp_utf8[500];

		FILE * FILE_FileKw;

		int m=0;
		FILE_FileKw=fopen(KwDeleteHtml->file,"r");
		if (FILE_FileKw == NULL) perror ("Error opening file");
		else
		{
			while ( ! feof (FILE_FileKw) )
			{
				if ( fgets (str_tmp, 1024 , FILE_FileKw) != NULL )
				{
					if(strlen(str_tmp) > 400 || strlen(str_tmp) <3 ) continue;


					Del_other_not_blank(str_tmp);
					m++;
					gb_to_utf8(str_tmp,str_tmp_utf8);
					if(strlen(str_tmp_utf8) != strlen(str_tmp))  m++;
				}
			}
			fclose (FILE_FileKw);

		}
		KwDeleteHtml->kw_arr = (char **) malloc(m * sizeof(char * ));
		printf("read_file_kw  m=[%d]\n" ,  m);
		m=0;
		FILE_FileKw=fopen(KwDeleteHtml->file,"r");
		if (FILE_FileKw == NULL) perror ("Error opening file");
		else
		{
			while ( ! feof (FILE_FileKw) )
			{
				if ( fgets (str_tmp, 1024 , FILE_FileKw) != NULL )
				{
					if(strlen(str_tmp) > 400 || strlen(str_tmp) <3 ) continue;


					Del_other_not_blank(str_tmp);
					gb_to_utf8(str_tmp,str_tmp_utf8);


					KwDeleteHtml->kw_arr[m] = (char * )malloc((strlen(str_tmp)+1) * sizeof(char ));
					sprintf(KwDeleteHtml->kw_arr[m] ,"%s" , str_tmp);
					printf("read_file_kw %2d  [%s]\n" ,m, KwDeleteHtml->kw_arr[m]);
					m++;
					if(strlen(str_tmp_utf8) != strlen(str_tmp))
					{
						KwDeleteHtml->kw_arr[m] = (char * )malloc((strlen(str_tmp_utf8)+1) * sizeof(char ));
						sprintf(KwDeleteHtml->kw_arr[m] ,"%s" , str_tmp_utf8);
						printf("read_file_kw %2d  [%s]\n" ,m, KwDeleteHtml->kw_arr[m]);
						m++;
					}




				}
			}
			fclose (FILE_FileKw);

		}
		printf("read_file_kw num=%d\n",m);
		return m;

}
*/
int read_file_kw_newnew(QListShieldWeb* QL,struct KWDELETEHTML *arr)//char *filename ,char **str_arr)
{

		printf("[read_file_kw-------------read_file_kw]\n") ;

		char str_tmp[500],str_tmp_utf8[500];
	 	int type = arr->type;
		FILE * FILE_FileKw;

		int m=0;
		//KwDeleteHtml->kw_arr = (char **) malloc(m * sizeof(char * ));
		printf("read_file_kw  m=[%d]\n" ,  m);
		m=0;
		FILE_FileKw=fopen(arr->file,"r");
		if (FILE_FileKw == NULL) perror ("Error opening file");
		else
		{
			while ( ! feof (FILE_FileKw) )
			{
				if ( fgets (str_tmp, 1024 , FILE_FileKw) != NULL )
				{
					if(strlen(str_tmp) > 400 || strlen(str_tmp) <3 ) continue;


					Del_other_not_blank(str_tmp);
					gb_to_utf8(str_tmp,str_tmp_utf8);

					strArrayInsert(&(QL->LinkArr[type] ) , &(QL->LinkArrNum[type]) , str_tmp);
					//KwDeleteHtml->kw_arr[m] = (char * )malloc((strlen(str_tmp)+1) * sizeof(char ));
					//sprintf(KwDeleteHtml->kw_arr[m] ,"%s" , str_tmp);
					//printf("read_file_kw %2d  [%s]\n" ,m, KwDeleteHtml->kw_arr[m]);
					m++;
					if(strlen(str_tmp_utf8) != strlen(str_tmp))
					{
						strArrayInsert(&(QL->LinkArr[type] ) , &(QL->LinkArrNum[type]) , str_tmp_utf8);
						//KwDeleteHtml->kw_arr[m] = (char * )malloc((strlen(str_tmp_utf8)+1) * sizeof(char ));
						//sprintf(KwDeleteHtml->kw_arr[m] ,"%s" , str_tmp_utf8);
						//printf("read_file_kw %2d  [%s]\n" ,m, KwDeleteHtml->kw_arr[m]);
						m++;
					}




				}
			}
			fclose (FILE_FileKw);

		}
		printf("read_file_kw num=%d\n",m);
		return m;

}

int free_str_arr(struct KWDELETEHTML *KwDeleteHtml)
{
	int i;

	for(i=0;i<KwDeleteHtml->num;i++)

	    free((void *)KwDeleteHtml->kw_arr[i]);

	free((void *)KwDeleteHtml->kw_arr);


}


int True_Toupper_Str(char *str)
{  //小写转大些

	 char *p;
	 p = str;
	while(*p!='\0')
	{
		*p=toupper(*p);
		p++;
	}

	return 0 ;
}
int True_Tolower_Str(char *str)
{  /* 将s字符串内的大写字母转换成小写字母*/

	 char *p;
	 p = str;
	while(*p!='\0')
	{
		*p=tolower(*p);
		p++;
	}

	return 0 ;
}




int query_md5_web_md5_no (MYSQL *conn,char *md5){
	int index = domainNotHave;
	MYSQL_RES *res ;
	MYSQL_ROW row;
	char sql[200];
	sprintf(sql, "SELECT  `index`  FROM  `manzhua`.`web_md5_no` WHERE `web_md5_no`.`md5` = CAST( 0x%s AS BINARY ) LIMIT 1", md5 );
	if (mysql_query ( conn, sql))  {
		 char  buf[1000];
		 printf("%s\n",sql);
		// sprintf(buf , "\n  :\n%s\n%s\n\n" ,sql ,mysql_error(conn));
		// write_error(buf,Work.Recordworkfile);
		 return -10;
    }

	res = mysql_store_result(conn);
	if(row = mysql_fetch_row(res)){
		index = atoi(row[0]);//strtoul (row[0], NULL, 0);
	}
	mysql_free_result(res); res = NULL;
	return index;

}



int CheckDBShieldAndQLShieldWeb(MYSQL *conn, char *link){

	//index  -1  直接屏蔽域名，>-1 是屏蔽动态数组队列中的数组下标
	//检查连接是否为屏蔽连接，包括域名屏蔽和小连接屏蔽
	//char link[200];
	//sprintf(link , "http://55570.sh.ylc93.com/uk/rh8c5/");
	if( 1 == checkWeb(link,"weibo.com")  || 1 == checkWeb(link,"mp.weixin.qq.com")  ) return YES;
	/*
	三种格式导出
	长网址 http://yizhifu8888.net/asdsd/        1        1107280        link
	域名 .ykdxb.com/        1        1107280        domain
	全网址(包括博客链接，和短域名链接http://51shangj.blog.51cto.com/    http://yizhifu8888.net/ ) http://yizhifu8888.net/         1        1107280        web

	*/

	char domain[100],md5[100];	//主域名  			http://news.sina.com.cn/dfdfe	=> sina.com.cn

	if(1 == getDomain( link, domain) ){
		int indexDB;
		md5_gen(md5,domain);
		indexDB = query_md5_web_md5_no (conn,md5 );
		if(domainNotHave  == indexDB )
			return 	YES;
		else if(domainOnly  == indexDB )
			return	NO;
		else{
			QNodeShieldWeb *node = QLShieldWeb->domainArr[indexDB];
			if(HAVE == QLShield_Domain_Check(QLShieldWeb,  node, link ,estarlink_all_bad))
				return NO;
		}
	}
	else{
		//取host 失败，应该返回1
		char buf[1000],filename[200];
		sprintf(buf,"getDomain error[%s]\n", link );
		sprintf(filename,"%s/getDomainError.txt",NowWorkingDir);
		RecordMessage(buf,filename,1);
		//sleep(1000000000);
		return NO;

	}
	return YES;
}

int SearchQLShieldWeb_by_database(MYSQL *conn, char *link){

	//检查连接是否为屏蔽连接，包括域名屏蔽和小连接屏蔽
	//char link[200];
	//sprintf(link , "http://55570.sh.ylc93.com/uk/rh8c5/");
	if( 1 == checkWeb(link,"weibo.com")  || 1 == checkWeb(link,"mp.weixin.qq.com")  ) return 0;
	/*
	三种格式导出
	长网址 http://yizhifu8888.net/asdsd/        1        1107280        link
	域名 .ykdxb.com/        1        1107280        domain
	全网址(包括博客链接，和短域名链接http://51shangj.blog.51cto.com/    http://yizhifu8888.net/ ) http://yizhifu8888.net/         1        1107280        web

	*/
	char host_bak[100], md5[100],buf[1000];
	char domain[100];	//主域名  			http://news.sina.com.cn/dfdfe	=> sina.com.cn
	char host[100]; 	//链接中的域名	   	http://news.sina.com.cn/dfdfe	=> news.sina.com.cn
	if(get_link_main(link , host) >0 )
	{
		//要检查2次
		char tmp[200];
		//域名屏蔽查询 .ykdxb.com/
		sprintf(host_bak, "%s" , host);
		if(1 == get_domain( host_bak, domain))
		{
			/*
			 if(strstr(link , ".ylc93.com/")){
				printf("[%s],[%s],[%s][%s]-----------\n",domain,host,link,md5);
			 }
			 */
			//**********************************************
			//网址域名  .sina.com.cn/
			//**********************************************
			//sprintf(tmp ,".%s",domain);
			md5_gen(md5,domain);
			if(query_md5_web_md5_no (conn,md5) > 0) {
				//printf("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaa\n");
				return HAVE;
			}
			else{
				// if(strstr(link , ".ylc93.com/")){
				//	sprintf(buf,"1[%s],[%s],[%s][%s][%s]\n",domain,host,link,tmp,md5);
				//	RecordMessage(buf,"/home/zran/src/manzhua23/ylc93.txt",1);

					/*
					domain =>[cdfpoh.ylc93.com],
					host =>[cdfpoh.ylc93.com],
					link => [http://cdfpoh.ylc93.com/]
					tmp => [.cdfpoh.ylc93.com/]
					md5=> [d4f73fcf0e7f433d862d5343d683da4a]

					domain =>[ctrip.com],
					host =>[dac4.sh.ylc93.com],
					link =>[http://dac4.sh.ylc93.com/class/banking/]
					tmp =>[.ctrip.com/]
					md5=>[62613a3e9af9a4350157067dfeb4908b]
					*/
				// }
			}
			//printf("bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb\n");
		}
		else{
				// if(strstr(link , ".ylc93.com/")){
				//	sprintf(buf,"2[%s],[%s],[%s]\n",domain,host,link );
				//	RecordMessage(buf,"/home/zran/src/manzhua23/ylc93.txt",1);
				// }

		}

		//**********************************************
		//网址查询  http://51shangj.blog.51cto.com/
		//**********************************************
		//sprintf(tmp ,"%s",host); //**********************************************************
		md5_gen_link(md5 , host); //域名入库时就是51shangj.blog.51cto.com
		if(query_md5_web_md5_no (conn,md5) > 0) return HAVE;
	}
	else{
		//取host 失败，应该返回1
		sprintf(buf,"get_link_main[%s]\n", link );
		RecordMessage(buf,"/home/zran/src/manzhua23/get_link_main_error.txt",1);
		//sleep(1000000000);
		return HAVE;
		/*
		 if(strstr(link , ".ylc93.com/")){
			sprintf(buf,"3[%s],[%s]\n", host,link );
			RecordMessage(buf,"/home/zran/src/manzhua23/ylc93.txt",1);
		 }
		 */
	}
	return NOTHAVE;
}
/***********************************************
* 检查连接中是否有域名
* checkDomain(link , "baidu.com")
************************************************/
int checkDomain(QNodeLink *node_now ,int layer, char * link){
	//if(NULL ==strstr(link ,"bitauto.com" ))
	//if(IsWeb != node_now->node_web->nodeWQ->type)
	//	printf("myid = %2d   type=%d [%s]  [%s] [%s]\n" ,node_now->threadinfo->myid ,node_now->node_web->nodeWQ->type,node_now->node_web->domain,node_now->node_web->link,link  );
	//if(IsWeb== node_now->node_web->nodeWQ->type){
	// 1 、检查是否出域了？
	if( NULL == strstr(link , node_now->node_web->domain )) //node_now->node_web->domainNode->domain &&
		return NO;

	//2、检查这个网站自己屏蔽的网址队列
	//if(HAVE == QLShield_Domain_LinkArrNO_Check(QLShieldWeb , node_now->node_web->domainNode,  link) )
	if(HAVE == QLShield_Domain_Check(QLShieldWeb , node_now->node_web->domainNode,  link ,estarlink_all_bad) )
		return NO;
	//3、公共屏蔽链接检查
	//if(HAVE == QLShieldPublicLinkCheck(QLShieldWeb , link) )
	if(HAVE == QLShield_PublicLink_Check(QLShieldWeb , Public_Shield_Link ,  link))
		return NO;
	//4、如果是采集末级链接，那么要判断  estarlink_end_good
	if( layer < 1  &&   NOTHAVE == QLShield_Domain_Check(QLShieldWeb , node_now->node_web->domainNode,  link ,estarlink_end_good) )
		return NO;
	//}

	return YES;

}

struct WEBINFO{ //存储网站信息的数组
	  char link[500];
	  unsigned int layer;
	  unsigned int id;
	  char web[100];
 };
 /**************************************************************************************
 * 网络来源网址入数组
 ***************************************************************************************/
int shield_domainAndHost_to_DB( MYSQL *conn, struct QListShieldWeb* QL,char *workfilepath) {


	  	//MYSQL *conn;
		//conn = mysql_conn_init("manzhua");
		char md5[50] ,*p,tmp[500],tmp2[500],domain[100];
		FILE *FILE_web_linkfile;
		struct WEBINFO Shieldwebinfo;
	       unsigned int i = 0,Shield_Num;
		int  line=-1,n_DB=0,n_QL=0,len;
		while(1){
	        	FILE_web_linkfile=fopen(  workfilepath,"r");
	        	if(FILE_web_linkfile==NULL)   {
						printf("can not find web_shield_to_array=%s\n", workfilepath);
						sleep(10);
						continue;
				}
				else
						break;
		}
		/*
		三种格式导出
		长网址 http://yizhifu8888.net/asdsd/ 	   1		1107280 	   link 		   http://finance.huagu.com/workdongjing
		域名 .ykdxb.com/		  1 	   1107280		  domain
		全网址(包括博客链接，和短域名链接http://51shangj.blog.51cto.com/	http://yizhifu8888.net/ ) http://yizhifu8888.net/		  1 	   1107280		  web
		读2次，先读domian和web
		*/

		// 1 、只记录屏蔽主域名记录,插入数据库
		line=-1;
		i = 0;
		while(!feof(FILE_web_linkfile)) {
				if(line<0)
						fscanf(FILE_web_linkfile,	"%d\n",&Shield_Num);
				else{
						fscanf(FILE_web_linkfile,	"%s %d %d %s\n",&Shieldwebinfo.link,&Shieldwebinfo.layer,&Shieldwebinfo.id,&Shieldwebinfo.web);

						//插入数据库
						if(0 == strcmp("domain" ,Shieldwebinfo.web)  || 0 == strcmp("web" ,Shieldwebinfo.web) ) {
								//统一各种域名形式，入库
								//剔除尾部'/'  http://www.sina.com.cn/ => http://www.sina.com.cn
								len = strlen(Shieldwebinfo.link);
								if( '/' == Shieldwebinfo.link[len -1])
										Shieldwebinfo.link[len-1] = '\0';
								//剔除首部'.'  .sina.com.cn  =>   sina.com.cn
								if( '.' == Shieldwebinfo.link[0]){
										p = Shieldwebinfo.link;
										p++;
										sprintf(tmp , "%s",p);
										sprintf(Shieldwebinfo.link , "%s",tmp);
								}

								if(0 == strcmp("web" ,Shieldwebinfo.web) ){
										if(1 == getDomain(Shieldwebinfo.link, domain)) {

											//判断这个web 是否是 屏蔽域名
											//删除://www.xxxx.xxx中www部分    http://www.sina.com.cn => sina.com.cn

											sprintf(tmp, "//www.%s", domain);
											sprintf(tmp2, "//%s", domain);
											//是主域名
											if(strstr(Shieldwebinfo.link, tmp)  ||  strstr(Shieldwebinfo.link ,tmp2) ){
												//domain已经赋值
											}
											//是二级域名
											else
												domain[0] = '\0';
										}
										else
											domain[0] = '\0';
								}
								else{
									sprintf(domain ,"%s" ,Shieldwebinfo.link);
								}

								if( '\0' != domain[0] ){
									md5_gen(md5 , domain ); //这个地方就是取://之后的信息
									int index_db = query_md5_web_md5_no( conn,  md5);
									if(domainNotHave == index_db)
										insert_web_md5_no( conn,   md5 ,domainOnly);
									n_DB++;
								}
						}
						i++;

				}
				line++;

		}
		//printf("22222222222222222222\n");
		//2、屏蔽web类中的二级域名,插入数据库
		line=-1;
		i = 0;
		fseek(FILE_web_linkfile, 0 , SEEK_SET);
		while(!feof(FILE_web_linkfile)) {
				if(line<0)
						fscanf(FILE_web_linkfile,	"%d\n",&Shield_Num);
				else{
						fscanf(FILE_web_linkfile,	"%s %d %d %s\n",&Shieldwebinfo.link,&Shieldwebinfo.layer,&Shieldwebinfo.id,&Shieldwebinfo.web);

						//插入domain队列
						if( 0 == strcmp("web" ,Shieldwebinfo.web) ) {
								//web类型，有可能屏蔽二级域名，所有必须加入doming屏蔽队列
								//统一各种域名形式，入库
								//剔除尾部'/'  http://www.sina.com.cn/ => http://www.sina.com.cn
								len = strlen(Shieldwebinfo.link);
								if( '/' == Shieldwebinfo.link[len -1])
										Shieldwebinfo.link[len-1] = '\0';

								if(1 == getDomain(Shieldwebinfo.link, domain)) {
									md5_gen(md5, domain);
									int index_db = query_md5_web_md5_no( conn,  md5);
									//库内有这个记录，而且是全屏蔽
									if(domainOnly  == index_db)
										continue;
									int domainIndex = QLShield_Domain_Link_Insert(QLShieldWeb, domain, Shieldwebinfo.link, estarlink_all_bad);

									//库内没有这个域名
									if(domainNotHave  == index_db){
										//下边只可能是二级域名，因为上一轮已经把主域名全都屏蔽了

										md5_gen(md5 , domain ); //这个地方就是取://之后的信息
										insert_web_md5_no( conn,   md5 ,domainIndex);
									}
									//库里有了这个域名，无需再插入
									else{

									}

								}
								n_DB++;


						}
						i++;

				}
				line++;

		}
		//printf("33333333333333333333\n");
		//3、屏蔽link类
		//将文件移动到开始位置
		line=-1;
		i = 0;
		fseek(FILE_web_linkfile, 0 , SEEK_SET);
		while(!feof(FILE_web_linkfile)) {
						if(line<0)
								fscanf(FILE_web_linkfile,	"%d\n",&Shield_Num);
						else{
								fscanf(FILE_web_linkfile,	"%s %d %d %s\n",&Shieldwebinfo.link,&Shieldwebinfo.layer,&Shieldwebinfo.id,&Shieldwebinfo.web);
								/*
								三种格式导出
								长网址 http://yizhifu8888.net/asdsd/ 	   1		1107280 	   link 		   http://finance.huagu.com/workdongjing
								域名 .ykdxb.com/		  1 	   1107280		  domain
								全网址(包括博客链接，和短域名链接http://51shangj.blog.51cto.com/	http://yizhifu8888.net/ ) http://yizhifu8888.net/		  1 	   1107280		  web

								*/

								 if(0 == strcmp("link" ,Shieldwebinfo.web)){
										//QNodeShieldWeb*  nodeLimit;
										if(strlen(Shieldwebinfo.link) < 100){
												if(1 == getDomain(Shieldwebinfo.link, domain)){
														md5_gen(md5, domain);
														int index_db = query_md5_web_md5_no( conn,  md5);
														if( domainOnly == index_db)
															continue;

														//只采集网站下的某种链接
														//if(1 == checkWeb(link , "www.zhihu.com")	&& NULL == strstr(link,"/question/") )	return 0;
														int type;
														if(strstr(Shieldwebinfo.link , estarlink[estarlink_end_good]) ){
																p =strstr(Shieldwebinfo.link , estarlink[estarlink_end_good]);
																p = p +strlen(estarlink[estarlink_end_good]);
																sprintf(Shieldwebinfo.link , p);
																type = estarlink_end_good;
														}
														else if(strstr(Shieldwebinfo.link , estarlink[estarlink_all_bad]) ){
																p =strstr(Shieldwebinfo.link , estarlink[estarlink_all_bad]);
																p = p +strlen(estarlink[estarlink_all_bad]);
																sprintf(Shieldwebinfo.link , p);
																type = estarlink_all_bad;
														}
														//普通屏蔽链接
														else{
																type = estarlink_all_bad;
														}

														int domainIndex = QLShield_Domain_Link_Insert(QLShieldWeb, domain, Shieldwebinfo.link, type);

														//数据库无记录
														if( domainNotHave  == index_db) {
															md5_gen(md5 , domain ); //这个地方就是取://之后的信息
															insert_web_md5_no( conn,   md5 , domainIndex);
														}
														//数据库有记录，有索引了
														else{

														}

												}
												n_QL++;
										}

								}

								i++;

						}
						line++;

				}

		fclose(FILE_web_linkfile);

		Shield_Num = i;
		//mysql_close(conn);
		printf("n_QL=%d    n_DB=%d\n" , n_QL,n_DB);
		return Shield_Num;
}
/*
int shield_link_to_ShieldWebQL( MYSQL *conn, struct QListShieldWeb* QL,char *workfilepath) {


	  	//MYSQL *conn;
		//conn = mysql_conn_init("manzhua");
		char md5[50] ,*p,tmp[500],tmp2[500],domain[100];
		FILE *FILE_web_linkfile;
		struct WEBINFO Shieldwebinfo;
	       unsigned long i = 0,Shield_Num;
		int  line=-1,n_DB=0,n_QL=0,len;
		while(1){
	        	FILE_web_linkfile=fopen(  workfilepath,"r");
	        	if(FILE_web_linkfile==NULL)   {
						printf("can not find web_shield_to_array=%s\n", workfilepath);
						sleep(10);
						continue;
				}
				else
						break;
		}

		//三种格式导出
		//长网址 http://yizhifu8888.net/asdsd/ 	   1		1107280 	   link 		   http://finance.huagu.com/workdongjing
		//域名 .ykdxb.com/		  1 	   1107280		  domain
		//全网址(包括博客链接，和短域名链接http://51shangj.blog.51cto.com/	http://yizhifu8888.net/ ) http://yizhifu8888.net/		  1 	   1107280		  web
		//读3次，先读domian和web，之后读link，link 要查询。


		//3、屏蔽link类
		//将文件移动到开始位置
		line=-1;
		i = 0;
		fseek(FILE_web_linkfile, 0 , SEEK_SET);
		while(!feof(FILE_web_linkfile)) {
						if(line<0)
								fscanf(FILE_web_linkfile,	"%u\n",&Shield_Num);
						else{
								fscanf(FILE_web_linkfile,	"%s %d %u %s\n",&Shieldwebinfo.link,&Shieldwebinfo.layer,&Shieldwebinfo.id,&Shieldwebinfo.web);

								//插入domain队列
								if( 0 == strcmp("web" ,Shieldwebinfo.web) ) {
										//web类型，有可能屏蔽二级域名，所有必须加入doming屏蔽队列
										//统一各种域名形式，入库
										//剔除尾部'/'  http://www.sina.com.cn/ => http://www.sina.com.cn
										len = strlen(Shieldwebinfo.link);
										if( '/' == Shieldwebinfo.link[len -1])
												Shieldwebinfo.link[len-1] = '\0';

										if(1 == getDomain(Shieldwebinfo.link, domain)) {

											//判断这个web 是否是 屏蔽域名
											//删除://www.xxxx.xxx中www部分    http://www.sina.com.cn => sina.com.cn

											sprintf(tmp, "//www.%s", domain);
											sprintf(tmp2, "//%s", domain);
											if(strstr(Shieldwebinfo.link, tmp)	||	strstr(Shieldwebinfo.link ,tmp2) ){
												//是屏蔽主域
												//sprintf(Shieldwebinfo.link , "%s",domain);
												domain[0] = '\0';
											}
											else{
												//向屏蔽队列，针对域名添加屏蔽链接。
												QLShield_Domain_Link_Insert(QLShieldWeb, domain, Shieldwebinfo.link, estarlink_all_bad);

											}
										}
										else
											domain[0] = '\0';

								}
								else if(0 == strcmp("link" ,Shieldwebinfo.web)){
										//QNodeShieldWeb*  nodeLimit;
										if(strlen(Shieldwebinfo.link) < 100){
												if(1 == getDomain(Shieldwebinfo.link, domain)){
														//寻找特殊标记屏蔽的后边链接
														//	if(strstr(link,".autohome.com.cn/") ){
														//			if(strstr(link,"order_") &&  strstr(link,"eid=")  &&  strstr(link,"Siteid=")) return 0;
														//	}


														//首先要查询数据库,如果这个链接的主域或二级域名已经被屏蔽了，那么就放弃这个链接
														if(HAVE == SearchQLShieldWeb_by_database(conn, Shieldwebinfo.link))
															continue;
														//屏蔽的链接主域节点可能在domain队列中没有，这是有可能的，所以必须先添加
														// QNodeShieldWeb*  nodeLimit= QLShield_Domain_Insert(QLShieldWeb, domain );


														//只采集网站下的某种链接
														//if(1 == checkWeb(link , "www.zhihu.com")	&& NULL == strstr(link,"/question/") )	return 0;
														p =strstr(Shieldwebinfo.link , estarlink[estarlink_end_good]);
														if(p ){
																p = p +strlen(estarlink[estarlink_end_good]);
																sprintf(Shieldwebinfo.link , p);
																QLShield_Domain_Link_Insert(QLShieldWeb, domain, Shieldwebinfo.link, estarlink_end_good);
														}
														else {
																//屏蔽域名下的特殊链接
																//if(strstr(link, ".fang.com/hezu/" ) || strstr(link, ".fang.com/chuzu/") || strstr(link, ".fang.com/house/"))	return 0;
																//http://www.fang.com/estarlink_all_bad=.fang.com/hezu/
																p = strstr(Shieldwebinfo.link , estarlink[estarlink_all_bad]);
																if( p ){
																		p = p +strlen(estarlink[estarlink_all_bad]);
																		sprintf(Shieldwebinfo.link , p);
																}
																//屏蔽域名下的普通链接
																//http://finance.huagu.com/workdongjing
																else{

																		//要单组一个队列，让出域的网址可以查询

																}
																//向屏蔽队列，针对域名添加屏蔽链接。
																QLShield_Domain_Link_Insert(QLShieldWeb, domain, Shieldwebinfo.link, estarlink_all_bad);


														}

														//将有限制的domain节点插入domainLimitArr数组中
														//QLShield_domainLimitArr_Insert(QLShieldWeb, nodeLimit);
												}
												n_QL++;
										}

								}

								i++;

						}
						line++;

				}

		fclose(FILE_web_linkfile);

		Shield_Num = i;
		//mysql_close(conn);
		printf("n_QL=%d    n_DB=%d\n" , n_QL,n_DB);
		return Shield_Num;
}
*/
int ReadcfgNew(struct QListWebQueue* QLWebAll ,  struct MYNUM * Num) //struct MYFILE * File,
{
	char *sourcestr ,*begin,*p,*psave, strreturn[200];
  	MYSQL *conn;
	conn = mysql_conn_init("manzhua");


	//确立numgoodproxy ，Num_QLWebAll 数量
	THREADINFO_Control_No = 0;
	Num->thread_all = 1; //统计线程
	Num->thread_download_index = 1;
	Num->goodproxy=0;
	Num->WebQueue = 0;
	Num->wget = 0;
	char name[1000],buf[1000];
	int i,j;
	char tmpbuf[200];
	char mydir[200];



	do_base_work(QLWebAll,Num);




	//----------------------------------------------------------------------------------
	//---------------------config.cfg----------------------------------------------------------
	//----------------------------------------------------------------------------------

	sourcestr = file2strzran("config.cfg");


	//是否下载网址信息--------------------------------------------------------------------

	int ifprint = 1,iffree = 0;

	begin = sourcestr;
	begin =  readinfo(begin,"Myip" ,Myip   ,Num ,ifprint);
	if(begin == NULL)   goto outReadcfg;

	begin =  readinfo(begin,"Targetdir" ,Targetdir  ,Num ,ifprint);
	if(begin == NULL)   goto outReadcfg;
	mkdir(Targetdir,0755);
	//清理目录Targetdir
	//sprintf(buf,"find %s -type f   |  grep -v \"_search*\" |  xargs rm -rf" , Targetdir);
	//sprintf(buf,"find %s -name '_iask*' -exec rm -rf {} \; " , Targetdir);
	sprintf(buf,"find %s -name '_iask*' |xargs  rm -rf ", Targetdir);
	system(buf);


	begin =  readinfo(begin,"Savedir" ,Savedir   ,Num ,ifprint);
	if(begin == NULL)   goto outReadcfg;
	sprintf( buf,"rm  %s -rf", Savedir);
	system(buf);
	mkdir(Savedir,0755);

	begin =  readinfo(begin,"Parseddir" ,Parseddir  ,Num ,ifprint);
	if(begin == NULL)   goto outReadcfg;
	sprintf( buf,"rm  %s -rf", Parseddir);
	system(buf);
	mkdir(Parseddir,0755);

	//Downdloadip-------------------------------------------------------------
	begin =  readinfo(begin,"Downdloadip" ,Downdloadip   ,Num ,ifprint);
	if(begin == NULL)   goto outReadcfg;

	//Port-------------------------------------------------------------
	begin =  readinfo(begin,"Port" ,strreturn  ,Num ,ifprint);
	if(begin == NULL)   goto outReadcfg;
	Port = atoi(strreturn);

	//限速设置-------------------------------------------------------------
	begin =  readinfo(begin,"LimitRate" ,strreturn  ,Num ,ifprint);
	if(begin == NULL)   goto outReadcfg;
	LimitRate = atoi(strreturn);

	//清理链接库采集间隔的天数---------------------------------------------------
	begin =  readinfo(begin,"CaiJiClearDays" ,strreturn  ,Num ,ifprint);
	if(begin == NULL)   goto outReadcfg;
	CaiJiClearDays = atoi(strreturn);
	CaiJiClearTime=CaiJiClearDays*24*3600;

	//大圈间隔时间，分钟转换秒------------------------------------------------
	begin =  readinfo(begin,"BigLoopIntervalTime" ,strreturn  ,Num ,ifprint);
	if(begin == NULL)   goto outReadcfg;
	BigLoopIntervalTime = atoi(strreturn) * 60;

	//每次重启时间RebootTime=1 ------------------------------------------------
	begin =  readinfo(begin,"RebootTime" ,strreturn  ,Num ,ifprint);
	if(begin == NULL)   goto outReadcfg;
	if(1 == strlen(strreturn))
		sprintf(RebootTime," 0%s:",strreturn);
	else if(2 == strlen(strreturn))
		sprintf(RebootTime," %s:",strreturn);
	else
	 	   goto outReadcfg;
	printf("RebootTime=[%s]\n",RebootTime);

	//调试模式----------------------------------------------------
	begin =  readinfo(begin,"MyDebug" ,strreturn ,Num ,ifprint);
	if(begin == NULL)   goto outReadcfg;
	MyDebug = atoi(strreturn);
	//是否调用汇总中心链接检查----------------------------------------------------
	begin =  readinfo(begin,"IfCheckCenter" ,strreturn ,Num ,ifprint);
	if(begin == NULL)   goto outReadcfg;
	IfCheckCenter = atoi(strreturn);

	//汇总中心链接----------------------------------------------------
	begin =  readinfo(begin,"CheckCenterLink" ,strreturn ,Num ,ifprint);
	if(begin == NULL)   goto outReadcfg;
	sprintf(CheckCenterLink,"%s",strreturn);

	/*
	//pppoe----------------------------------------------------
	begin =  readinfo(begin,"PPPOE" ,strreturn ,Num ,ifprint);
	if(begin == NULL)   goto outReadcfg;
	PPPOE= atoi(strreturn);
	*/
	//--------------------------------------------------------------------------
	//download_a_file(KwDeleteHtml.file,1 );
	//KwDeleteHtml.num = read_file_kw(&KwDeleteHtml);
	//网址屏蔽链接，必须在所有常规网址采集入列后进行，因为，他要寻找domain，添加屏蔽网址
	download_a_file(ShieldWeb_file,1 );
	shield_domainAndHost_to_DB(  conn, QLShieldWeb,ShieldWeb_file) ;
	//QLShield_Domains_Display(QLShieldWeb , "qq.com");
	//QLShield_Domains_Display(QLShieldWeb , "sdbgw.com.cn");
	//sleep(1000);
	//QLShield_domainLimitArr_Display(QLShieldWeb ); sleep(100);
	//屏蔽文件中link部分加入domain中
	//shield_link_to_ShieldWebQL( conn, QLShieldWeb,ShieldWeb_file) ;
	//QLShield_domainLimitArr_Display(QLShieldWeb ); sleep(100);


	//-------------------------------------------------------------------------------------
	//-------------------------------------------------------------------------------------
	//-------------------------------------------------------------------------------------
	struct CONFIGSET config;
	char *end;
	iffree =1;
	begin = sourcestr;
	while(1)
	{
		printf("---------------------------------------------\n\n");
		p = strstr(begin,"Num_Download_Thread");
		if(p)
		{
			end = strstr(begin,"QueueEnd");
			if(end)
			{
				*end = '\0';
				p = begin;
				config.num_thread =0;

				p =  readinfo(  p,"Num_Download_Thread" ,strreturn ,Num ,ifprint);
				if( p) config.num_thread  = atoi(strreturn);


				if(config.num_thread  >0)
				{

						//type
						p = readinfo(  p,"QueueType" ,strreturn   ,Num ,ifprint);
						if(p == NULL)  break;

						if(strstr(strreturn ,"web") ) config.type = IsWeb;
						else if(strstr(strreturn ,"weibo") ) config.type = IsWeibo;
						else if(strstr(strreturn ,"weixin") ) config.type = IsWeiXin;
						else if(strstr(strreturn ,"search") ) config.type = IsSearch;
						else   {printf("ReadcfgNew is error QueueType no\n");Num->WebQueue = 0;   break;}

						//Tools  //{"wget","PhantomjsWeb","PhantomjsAll ","ChromePythonWeb","ChromePythonAll","ChromeCommandWeb","ChromeCommandAll","ServerWeb","ServerAll"};
						p = readinfo(  p,"Tools" ,strreturn  ,Num ,ifprint);
						if(p == NULL ) break;
						if(   0 == strcmp(strreturn ,"wget") )						config.Tools = ToolsWget;
						else if(0 == strcmp(strreturn ,"PhantomjsWeb") )		config.Tools = ToolsPhantomjsWeb;
						else if(0 == strcmp(strreturn ,"PhantomjsAll") )		config.Tools = ToolsPhantomjsAll;
						else if(0 == strcmp(strreturn ,"ChromePythonWeb") )		config.Tools = ToolsChromePythonWeb;
						else if(0 == strcmp(strreturn ,"ChromePythonAll") )		config.Tools = ToolsChromePythonAll;
						else if(0 == strcmp(strreturn ,"ChromeCommandWeb") )	config.Tools = ToolsChromeCommandWeb;
						else if(0 == strcmp(strreturn ,"ChromeCommandAll") )	config.Tools = ToolsChromeCommandAll;
						else if(0 == strcmp(strreturn ,"DirServerWeb") )			config.Tools = ToolsDirServerWeb;
						else if(0 == strcmp(strreturn ,"DirServerAll") )			config.Tools = ToolsDirServerAll;
						else if(0 == strcmp(strreturn ,"WebServerWeb") )			config.Tools = ToolsWebServerWeb;
						else if(0 == strcmp(strreturn ,"WebServerAll") )			config.Tools = ToolsWebServerAll;
						else   {printf("ReadcfgNew is error Tools no [%s]\n",strreturn);Num->WebQueue = 0; sleep(10000);  break;}


						//Connection  const char *ConnectionStr[]={"direct ","proxy_web","proxy_all ","pppoe_web","pppoe_all"};
						p = readinfo(  p,"Connection" ,strreturn  ,Num ,ifprint);
						if(p == NULL ) break;
						if(strstr(strreturn ,"direct") )			config.Connection = Connection_direct;
						else if(strstr(strreturn ,"proxy_web") )	config.Connection = Connection_proxy_web;
						else if(strstr(strreturn ,"proxy_all") )	config.Connection = Connection_proxy_all;
						else if(strstr(strreturn ,"pppoe_web") )	config.Connection = Connection_pppoe_web;
						else if(strstr(strreturn ,"pppoe_all") )	config.Connection = Connection_pppoe_all;
						else   {printf("ReadcfgNew is error Connection no\n");Num->WebQueue = 0; sleep(10000);  break;}

						//webServer 此项目可以不填，默认是本机地址
						psave= p;
						p = readinfo(  p,"webServer" ,strreturn  ,Num ,ifprint);
						if(p == NULL ) {
							strcpy(config.webServer,"127.0.0.1:6081");
							p = psave;
						}
						else
							strcpy(config.webServer,strreturn);


						//IfDownload
						p = readinfo(  p,"IfDownload" ,strreturn   ,Num ,ifprint);
						if(p == NULL ) break;
						config.IfDownload = atoi(strreturn);


						//FileWeb
						p = readinfo(  p,"FileWeb" ,config.FileWeb  ,Num ,ifprint);
						if(p == NULL ) break;
						download_a_file(config.FileWeb,config.IfDownload  );

						//FileKw
						//p = readinfo(  p,"FileKw" ,config.FileKw  ,Num ,ifprint);
						//if(p == NULL ) break;
						//if( config.type != IsWeb ) download_a_file(config.FileKw,config.IfDownload  );


						//ServerNum
						p = readinfo(  p,"ServerNum" ,strreturn  ,Num ,ifprint);
						if(p == NULL ) break;
						config.ServerNum = atoi(strreturn);

						//ServerOrder
						p = readinfo(  p,"ServerOrder" ,strreturn   ,Num ,ifprint);
						if(p == NULL ) break;
						config.ServerOrder = atoi(strreturn);


						//NumSHInThread
						p = readinfo(  p,"NumSHInThread" ,strreturn   ,Num ,ifprint);
						if(p == NULL ) break;
						config.NumSHInThread = atoi(strreturn);

						//NumWgetInSH
						p = readinfo(  p,"NumWgetInSH" ,strreturn   ,Num ,ifprint);
						if(p == NULL ) break;
						config.NumWgetInSH = atoi(strreturn);

						//IntervalTimeWeb
						p = readinfo(  p,"IntervalTimeWeb" ,strreturn   ,Num ,ifprint);
						if(p == NULL ) break;
						config.IntervalTimeWeb = atoi(strreturn);


						//WgetTimeOut
						p = readinfo(  p,"WgetTimeOut" ,strreturn   ,Num ,ifprint);
						if(p == NULL ) break;
						config.WgetTimeOut = atoi(strreturn);

						create_nodeWQ(QLWebAll ,&config , Num);


				}



				*end = 'Q';
				begin = end +5;
				//break;
			}
			else
				break;

		}
		else
			break;

	}


	//读最后写文件时屏蔽的链接关键词，现在也废弃了
	/*
	download_a_file(UrlPingBiInEnd.file,1 );
	UrlPingBiInEnd.num = read_file_kw(&UrlPingBiInEnd);
	QLShield_PublicLink_Insert(QLShieldWeb, Public_Shield_EndLink , &UrlPingBiInEnd);
	QLShield_PublicLink_Display(QLShieldWeb ,Public_Shield_EndLink);
	*/

	download_a_file(KwArr[Public_Shield_EndLink].file,1 );
	read_file_kw_newnew( QLShieldWeb ,&KwArr[Public_Shield_EndLink] );
	//QLShield_PublicLink_Display(QLShieldWeb ,Public_Shield_EndLink);


	//读公共屏蔽链接
	/*
	download_a_file(UrlPingBiInPublic.file,1 );
	UrlPingBiInPublic.num = read_file_kw(&UrlPingBiInPublic);
	QLShield_PublicLink_Insert(QLShieldWeb, Public_Shield_Link , &UrlPingBiInPublic);
	QLShield_PublicLink_Display(QLShieldWeb ,Public_Shield_Link);
	*/
	download_a_file(KwArr[Public_Shield_Link].file,1 );
	read_file_kw_newnew( QLShieldWeb ,&KwArr[Public_Shield_Link] );
	//QLShield_PublicLink_Display(QLShieldWeb ,Public_Shield_Link);


	//采集文件类型屏蔽
	download_a_file(KwArr[Public_Shield_FileType].file,1 );
	read_file_kw_newnew( QLShieldWeb ,&KwArr[Public_Shield_FileType] );
	//QLShield_PublicLink_Display(QLShieldWeb ,Public_Shield_FileType);




	//加一个代理服务器处理线程
	THREADINFO_Proxy_No	 = Num->thread_all;
	Num->thread_all++;
	//加一个代理服务器处理线程工作目录
	char proxyworkdir[200];
	sprintf(proxyworkdir,"%s/proxy",NowWorkingDir);
	sprintf( buf,"rm  %s/2* -rf",proxyworkdir );
	system(buf);
	mkdir(proxyworkdir,0755);

	//char  mydir[200];
	for(i=0;i<Num->thread_all;i++)//创建各个线程的子目录
	{
		sprintf(mydir,"%s%d",Targetdir,i);
		mkdir(mydir,0755);

		sprintf(mydir,"%s%d",Savedir,i);
		mkdir(mydir,0755);
	}

	//printf("Num_Thread=%d   (Num_Download_Web=%d,WeiBo=%d    thread_weibo_search=%d ,WeiXin=%d,Search=%d  control =1 proxy=1)\n",Num->thread_all, Num->thread_web,Num->thread_weibo,Num->thread_weibo_search - 1,Num->thread_weixin,Num->thread_search);




	//printf("Num_WebQueue =  %d------------\n" ,Num->WebQueue    );
	//QLWebAll = (struct QListWebAll *) malloc ( sizeof(struct QListWebAll) * Num->QLWebAll );


outReadcfg:

	free(sourcestr);
	sourcestr = NULL;
	sleep(1);
	mysql_close(conn);
	return Num->WebQueue;

}

int getstr_cutsomestr(char *str,char *begin , char *end)
{
	//getstr_cutsomestr("javascript:winopen('http://www.aastocks.com/sc/news/HK6/NOW.563547/Count3.html'", "javascript:winopen('", "'")
	//输入 )
	//输出 http://www.aastocks.com/sc/news/HK6/NOW.563547/Count3.html
	if(strstr(str,begin))
	{
		char tmpp[1000],*p,*pp;
		p= str + strlen(begin);
		pp =  strstr(p , end);
		if(pp)
		{
			*pp = '\0';
			sprintf(tmpp,"%s" , p);
			sprintf(str,"%s" , tmpp);
			return 1;
		}
	}

	return 0;

}




/********************************************************************************
* 刚提取的链接做一些基本的初步检查
*********************************************************************************/
int checkLinkFirst(char *link , int  len){
	//1、链接长度检查
	if(len > 499) return 0;
	//2、链接末尾字符检查
	if(link[len-1]=='\\'  || link[len-1]=='?' )  return 0;  //http://v.wxrb.com/%5C%22%22+data5D97fG[i].url+%22#InterviewVideo\
	if(   !isalnum(link[8]) )  return 0; //http://[img=][img=]
	//3、链接后缀检查
	//if(0 == CheckFileType(link)) return 0;

	if(HAVE == QLShield_FileType_Check(QLShieldWeb , link))
		return 0;
	if(NULL != strstr(link,"javascript") ){
		//不可以直接屏蔽，比如http://www.aastocks.com/sc/default.aspx这个页面的连接是<a id="cp_lnkMostReadNews" class="h3 cls" href="javascript:winopen('http://www.aastocks.com/sc/news/HK6/NOW.563547/Count3.html')">
		//20130905

		if(getstr_cutsomestr(link, "javascript:winopen('", "')") <1 ) return 0;
	}

	//if(strstr(link,".3158.cn") ){
	//	if(NULL == strstr(link,"/news/") &&  NULL == strstr(link,"/info/")) return 0;
	//}
	//if(strstr(link,".anjuke.com") ){
	//	if(NULL == strstr(link,"/news/") &&  NULL == strstr(link,"/market/")) return 0;
	//}
	if(strstr(link,".autohome.com.cn/") ){
		if(strstr(link,"order_") &&  strstr(link,"eid=")  &&  strstr(link,"Siteid=")) return 0;
	}

	//4、特殊字符检查
	if(index(link,'"') || index(link,'\'')   || index(link,'<')    || index(link,'>')   || index(link,'{')    || index(link,'}')   || index(link,'$')  || index(link,'(')  )  return 0;

	//http://cn.agropages.com/mailto:info@agropages.com
	if(strstr(link,"mailto:") ) return 0;

	return 1;
}
/************************************************************************
//检查搜索引擎链接
*************************************************************************/
int CheckLinkSearch(MYSQL *conn,struct QNodeLink * nodelink , char *link  ,int layer  ){
	if( IsWeiXin == nodelink->node_web->nodeWQ->type ) {
		//http://mp.weixin.qq.com/profile
		if(0 == checkWeb(link , "mp.weixin.qq.com/s?"))// &&  0 == checkWeb(link,"weixin.sogou.com/websearch/art.jsp") )
			return NO;
	}
	else if( IsWeibo == nodelink->node_web->nodeWQ->type   ){

	}
	else if( IsSearch == nodelink->node_web->nodeWQ->type   ) {
		//if(strstr(link,"bing.com")) printf("1[%s]\n" , link);
		char *web = nodelink->threadinfo->nodeWQ->web;
		if(web){
			//百度贴吧必须提取自己的链接，其他链接无意义
			if( 0 == strcmp(web,"tieba.baidu.com") ){
				return  checkWeb(link,"tieba.baidu.com/p/") ;
			}
			else{
				//新浪搜索含有自身的信息，需要单独处理
				if( 0 == strcmp(web,"search.sina.com.cn") )
					return	!checkWeb(link,"search.sina.com.cn") ;

				if( strstr(nodelink->threadinfo->nodeWQ->web,".sogou.com") ) {
				   //屏蔽Sogou快照
				   if( strstr(link,".sogoucdn.com") )
					   return NO;
				}
				//屏蔽所有引擎提取练级中含有自己的链接。很对。
				char *p= index(nodelink->threadinfo->nodeWQ->web,'.');
				p++;
				if( strstr(link,p))
					return NO;

				//b、公共屏蔽链接检查
				if(HAVE == QLShield_PublicLink_Check(QLShieldWeb , Public_Shield_Link , link))
					return NO;

				//搜索引擎要进行全面检查
				if(NO == CheckDBShieldAndQLShieldWeb(  conn,   link))
					return NO;
			}
		}
		//if(strstr(link,"bing.com")) printf("2[%s]\n" , link);
	}
	return YES;
}
/************************************************************************
//检查出域的链接
*************************************************************************/
int CheckDomainOut(MYSQL *conn,struct QNodeLink * node_father , char *link  ,int layer ){

	// 1 、域内
	if( strstr(link , node_father->node_web->domain )){

		//a、检查这个网站自己屏蔽的网址队列
		if(HAVE == QLShield_Domain_Check(QLShieldWeb , node_father->node_web->domainNode,  link ,estarlink_all_bad) )
			return NO;

		//b、公共屏蔽链接检查
		if(HAVE == QLShield_PublicLink_Check(QLShieldWeb , Public_Shield_Link ,  link))
			return NO;

		//c、如果是采集末级链接，那么要判断  estarlink_end_good
		if( layer < 1  &&   NOTHAVE == QLShield_Domain_Check(QLShieldWeb , node_father->node_web->domainNode,  link ,estarlink_end_good) )
			return NO;
	}
	//2 域外
	else{
		//b、公共屏蔽链接检查
		if(HAVE == QLShield_PublicLink_Check(QLShieldWeb , Public_Shield_Link ,  link))
			return NO;

		//屏蔽数据库和屏蔽队列联合检查
		if( NO  == CheckDBShieldAndQLShieldWeb(conn , link)  )
			return NO;
	}
	return YES;

}

/************************************************************************
//合并主链接是目录
*************************************************************************/
void merge_url_dir(char *url_main , char *url_sub ,char *url_dest){
	//http://epaper.anhuinews.com/html/ahfzb/20180919  href="../../js/calendar.css"
	//http://epaper.anhuinews.com/html/ahfzb/20180919/  href="../../js/calendar.css"
	//http://www.sdenews.com/list     ../../../../html/2018/9/246882.shtml
	int len = strlen(url_main);
	char url_main_bak[len+1];
	strcpy(url_main_bak,url_main);
	char *p_main_bak = url_main_bak;
	if( '/' == url_main_bak[len -1] )
		url_main_bak[len -1] = '\0';

	char *p , *pp , *p_url_sub_save=url_sub;

	while(1){
		p = strstr(p_url_sub_save,"../");
		if(p){
			p_url_sub_save = p +3;
			pp = rindex(url_main_bak,'/');
			if(NULL == pp)
				 break;
			else{
				if(pp >p_main_bak && '/' != *(pp-1))
					*pp = '\0';
			}
		}
		else{
			//sprintf(url_dest , "%s/%s" , url_main_bak , p_url_sub_save );
			break;
		}
	}
	sprintf(url_dest , "%s/%s" , url_main_bak , p_url_sub_save );
}

char *parse_link(MYSQL *conn, int myid, char *srchttp , char *begin  ,   struct LINKTITLE *linktitle  ,int *parse_link_return , struct QNodeLink *node_now)
{
	/*
	        <li><a class="cart" href="http://jc.sh.tg.com.cn/index.php?c=cart/cart&m=viewcart" target="_blank"><span id="shopping_car">>
	璐墿杞?/span></a></li>^M
	        <li><a href="http://shop.tg.com.cn/user/index.php?c=order/order_search" target="_blank">鎴戠殑璁㈠崟<span id='my_order'></sp
	an></a></li>^M
	        <li><a href="http://shop.tg.com.cn/user/index.php?c=point/point" target="_blank">鎴戠殑绉垎</a></li>^M
	        <li><a href="http://shop.tg.com.cn/user/index.php" target="_blank">鎴戠殑榻愬</a></li>^M
	        <li><a href="http://jinan.tg.com.cn/help" target="_blank">甯姪涓績</a></li>^M
	        <li><a href="javascript:void(0);" id="L_freemail" onclick="LoginSelect('freemail')">免费邮箱</a>
	        //<link type="text/css" rel="stylesheet" href="http://www.sohu.com/upload/style/global1212.css" />
	*/
	/*
	寻找"<a",再找"href"

	*/
	int len;
	char *p, *linkbegin , *linkend, *titlebegin,*titleend ,c,*ppp;
	char *firstx,*pp,*thisp;
	char mylink[1000];
	 *parse_link_return = 0 ;
	thisp= begin;
	while(1)
		{
				// <link href="http://icon.zol-img.com.cn/dealer/css/style_new.css" rel="stylesheet" type="text/css" />
				// <base href="http://icon.zol-img.com.cn/dealer/css/style_new.css" rel="stylesheet" type="text/css" />
				//<a  target="_blank" href="http://anjj.xjbz.gov.cn/html/news/tpxw/2011-4/22/19_42_14_154.html" title="自治区安全生产监察总队对巴州
				/*
				p = index(thisp  , '<' );
				if(p == NULL) { *parse_link_return = -1 ;    return begin;}
				if(*(p+1) == 'a' || *(p+1) == 'A')
				{


				}
				*/


				p = strstr(thisp  , "<a " );
				if(p == NULL) { *parse_link_return = -1 ;    return begin;}
				p--;
				p = strstr(thisp  , " href=" );
				if(p == NULL) { *parse_link_return = -1 ;    return begin;}

				p = p+6;
				linkbegin = p + 1;

				//<a name="resHomeLeftEduPic" pos="1" href="'+arrWeb1[0].url+'" target="_blank">
				if(*linkbegin == '\'') { thisp =linkbegin + 1; continue;  }

				//a href="javascript:void(0);"
				if( *linkbegin =='j' && *(linkbegin+1) =='a'  && *(linkbegin+2) =='v' && *(linkbegin+3) =='a' && *(linkbegin+4) =='s' && *(linkbegin+5) =='c' && *(linkbegin+6) =='r' && *(linkbegin+7) =='i' && *(linkbegin+8) =='p' && *(linkbegin+9) =='t' )
					{thisp = linkbegin+6; continue;   }

				if(*p != '\"' && *p != '\'')
				{ //<a href=list.php?cid=181>政法学院简介</a>  <a href=http://www.yxnu.net/p_gbook/index.php  target=_blank>
					//thisp =p+1;continue;
					linkbegin = p ; //20160823
					p++;
					while(*p != '\0'  &&  *p != ' '  &&  *p != '>')
					{
						p++;
					}
					if(*p == '\0')  { *parse_link_return = -1 ;    return begin;}
					else linkend = p;
				}
				else
				{
					c = *p;
					linkend = index(linkbegin , c);
					if(linkend  == NULL)   { *parse_link_return = -1 ;    return begin;}
				}
				//<a name="res1095" pos="2" href="" target="_blank">  <a name="res1139" pos="1" href="#" target="_blank"></a>
				if(linkend -linkbegin <2)     {thisp =linkend+1; continue;   }

				if(linkend-linkbegin>499)     {thisp =linkend+1;   continue;   }

				strncpy(linktitle->link,linkbegin ,linkend-linkbegin);
				linktitle->link[linkend-linkbegin] = '\0';

				p = index(linkend , '>');
				if(p==NULL)  { *parse_link_return = -1 ;    return begin;}

				titlebegin = p+1;
				titleend = strstr(titlebegin , "</a>");
				if(titleend==NULL)  { *parse_link_return = -1 ;    return begin;}


				if(titleend-titlebegin > 4999)   { thisp = titleend+1; continue;   }
				strncpy(linktitle->title,titlebegin ,titleend-titlebegin);
				linktitle->title[titleend-titlebegin] = '\0';
				//Del_str_bengin_to_end_new(linktitle->title , "<",	">");
				Del_Tag(linktitle->title );
				//的确有些标题是空的，比如图片连接，没有文字，只有图片，那么就是空
				//len = strlen(linktitle->title);
				//if(len>499)   { thisp= titleend+1; continue;   }
				linktitle->title[500] = '\0';
				//if(MyDebug > 0) printf("[%s]\n",linktitle->link);

				len = strlen(linktitle->link);
				if(len>499 || len < 8)   { thisp= titleend+1; continue;   }


				Del_other(linktitle->link);
				convert_unicode(linktitle->link);
				/*
				//替换HTTP://  20160823
				if(strlen(linktitle->link) >7 && linktitle->link[0]=='H' && linktitle->link[1]=='T' && linktitle->link[2]=='T' && linktitle->link[3]=='P' && linktitle->link[4]==':' && linktitle->link[5]=='/' && linktitle->link[6]=='/'){
					linktitle->link[0]='h' ;
					linktitle->link[1]='t' ;
					linktitle->link[2]='t' ;
					linktitle->link[3]='p' ;
				}

				if(strlen(linktitle->link) >7 && linktitle->link[0]=='H' && linktitle->link[1]=='T' && linktitle->link[2]=='T' && linktitle->link[3]=='P'  && linktitle->link[4]=='S' && linktitle->link[5]==':' && linktitle->link[6]=='/' && linktitle->link[7]=='/'){
					linktitle->link[0]='h' ;
					linktitle->link[1]='t' ;
					linktitle->link[2]='t' ;
					linktitle->link[3]='p' ;
					linktitle->link[4]='s' ;
				}
				*/
				//替换大写http 为小写
				p = index(linktitle->link,':');
				if(p){
					*p = '\0';
					New_Tolower_Str(linktitle->link);
					*p = ':';
				}

				//ReplaceStr(linktitle->link,"&amp;","&");
				//链接检查
				len = strlen(linktitle->link);
				/*
				if(checkLinkFirst(linktitle->link , len) <1 || checkLinkSecond(conn,QLShieldWeb,linktitle->link) <1 ) {
					thisp= titleend+1;
					continue;
				}
				*/
				//由于--convert-links  会把文件名作为链接替换下载链接，必须加以过滤 ,是不采集链接解析为下载的文件名，有待再查
				if(strstr(linktitle->link,  node_now->threadinfo->_son_wget_info)  )   {
					//printf("0---[%s]\n[%s]\n[%s]\n" ,node_now->threadinfo->wget_html, node_now->linknew,linktitle->link );
					//sleep(1000);
					 thisp= titleend+1;
					continue;
				}
				/*****************************************************************
					遗留问题 20180925
					<a href="//weibo.com/3806727407/GAGHDbjBh?refer_flag=1001030103_" target="_blank">09月23日 15:45</a>
					这种'//'开始的子链接没有处理，wget可以自动转换，python的urllib.parse.urljoin()也可以自动转换，现在不是大问题，但是个缺陷
				******************************************************************/
				if(linktitle->link[0]=='h' && linktitle->link[1]=='t' && linktitle->link[2]=='t' && linktitle->link[3]=='p' &&
					(   linktitle->link[4]==':' && linktitle->link[5]=='/' && linktitle->link[6]=='/' || 							//http://
						linktitle->link[4]=='s' && linktitle->link[5]==':' && linktitle->link[6]=='/' && linktitle->link[7]=='/'	//https://
					)
				 ) {
			 			//如果是独立域名，那么结尾删除"/"
			 			 ppp = linktitle->link;
						 ppp = index(ppp+8,'/') ;
						 if( ppp!= NULL && *(ppp+1) == '\0' ) {linktitle->link[len-1] = '\0';}
						 //wget也有解析错误的时候。http:///stock.stockstar.com/report/
						 ReplaceStr(linktitle->link,":///","://");

						 *parse_link_return = 1 ;
						  return   titleend+1;
			 	}
				else
				{        // printf("aaaaaaaaaa[%s]\n",linktitle->link);
						//规则1
						firstx = index(srchttp+8,'/');
						sprintf(mylink , "%s" , linktitle->link);
						//主链接尾部没有'/'
						if(firstx == NULL )  // http://www.wenzhou315.gov.cn        /view_qygg.php?id=49699
						{
							//printf("\n\n%s\n%s\n" ,srchttp,linktitle->link );
							if(linktitle->link[0] == '.'  && linktitle->link[1] == '.'  && linktitle->link[2] == '/'  ) //http://www.testcenter.gov.cn/../Shop/goshoping.aspx?ProductID=125
							{
								pp = mylink;
								pp = pp +2;
								sprintf(linktitle->link , "%s%s",srchttp,pp);
							}
							else if(linktitle->link[0] == '.'  && linktitle->link[1] == '/'  )  //http://www.tongcheng.gov.cn  ./zwgk/news_view.php?id=14668&ty=1018
							{
								pp = mylink;
								pp++;
								sprintf(linktitle->link , "%s%s",srchttp,pp);
							}
							else if(linktitle->link[0] == '/')
								sprintf(linktitle->link , "%s%s",srchttp,mylink);
							else
								sprintf(linktitle->link , "%s/%s",srchttp,mylink);

							*parse_link_return = 1 ;
							return   titleend+ 1;

						}
						//主链接尾部有'/'
						else if( *(firstx+1) == '\0')   // http://www.wenzhou315.gov.cn/       view_qygg.php?id=49699
						{
							if(linktitle->link[0] == '/')
							{
								pp = mylink;
								pp++;
								sprintf(linktitle->link , "%s%s",srchttp,pp);
							}
							else sprintf(linktitle->link , "%s%s",srchttp,mylink);

							*parse_link_return = 1 ;
							return   titleend+ 1;

						}
						//主域名后还有/和一些字符，比如 // http://www.yicai.com/newspage/list/index-6.html      /news/2011/04/747928.html
						else {
							//子链接是/开头的，难么直接去父链接的一级域名
						 	if(linktitle->link[0]== '/')
					 		{
								*firstx = '\0';
								sprintf(linktitle->link , "%s%s",srchttp,mylink);
								*firstx = '/';
								*parse_link_return = 1 ;
								return   titleend+ 1;
					 		}
							//子连接不是/开头
							else{


								char *srchttp_tail = rindex(srchttp,'/');

								//主连接尾部是'/'
								if(*(srchttp_tail+1) == '\0'){      //http://epaper.anhuinews.com/html/ahrb/20180919/     index_1.shtml   ok
									merge_url_dir(srchttp , mylink ,linktitle->link);
									*parse_link_return = 1 ;
									return	 titleend+ 1;
								}
								//主连接尾部不是'/'
								else{
									//是页面
									if(index(srchttp_tail , '.')){  //20180920  //http://epaper.anhuinews.com/html/jhsb.shtml 	jhsb/20180918/index_1.shtml ok //http://epaper.anhuinews.com/html/hs/20150104/index_13.shtml  index_5.shtml  ok
										*srchttp_tail = '\0';
										//sprintf(linktitle->link , "%s/%s",srchttp,mylink);
										merge_url_dir(srchttp , mylink ,linktitle->link);
										*srchttp_tail = '/';
										*parse_link_return = 1 ;
										return	 titleend+ 1;
									}
									//是目录
									else{ //http://epaper.anhuinews.com/html/ahrb/20180919	   index_1.shtml  ok
										merge_url_dir(srchttp , mylink ,linktitle->link);
										*parse_link_return = 1 ;
										return	 titleend+ 1;
									}
								}

								/*
								{ //原来
								 	thisp =titleend+1;
								 	continue;
								}
								*/
							}
						}

						 //printf("\n\n%s\n%s\n%s\n\n" ,srchttp, mylink,linktitle->link );

				}
/*
				len = strlen(linktitle->link);
				if(checkLinkFirst(linktitle->link , len) <1 || checkLinkSecond(conn,QLShieldWeb,linktitle->link) <1 ) {
					thisp= titleend+1;
					continue;
				}
*/
		}

		*parse_link_return = 0;
		return thisp;
}

/************************************************************************
//删除字符串中的标签
【<em><!--red_beg-->小镇<!--red_end--></em>新闻】福州·<em><!--red_beg-->马尾基金小镇参与承办<!--red_end--></em>中国物流信息化大会投融资分论坛活动取得圆满成功

*************************************************************************/
int Del_Tag(char *str )
{

	//原来的程序，在64位下有问题，已修改位安全模式.20180715
	//对于大于小于号的判断，待测试
	//  printf("Del_str_bengin_to_end_newnew  begin[%s]\n",str);

	char *pbegin,*pend,*beginstr;
	beginstr = str;
	while(1){
		pbegin=index(beginstr,'<');
		if(pbegin==NULL) break;
		pend=index(pbegin+1 ,'>');
		if(pend==NULL) break;
		pend = pend +1;
		//</em> 删除这标签前边的空格
		if('/' == *(pbegin+1) ){
			if(pbegin > str && ' ' == *(pbegin-1))
				pbegin--;
		}
		//<em>删除整个标签后边的空格
		else{
			if(' ' == *pend )
				pend++;
		}

		beginstr = pbegin;
		while('\0' != *pend){
			*pbegin =*pend;
			pbegin++;
			pend++;
		}
		*pbegin= '\0';
	}
	 // printf("Del_str_bengin_to_end_newnew  end[%s]\n",str);


}

int Del_str_bengin_to_end_new(char *str,char *begin,char *end)
{
		 /*
		//删除字符串中，其实字符串到最后字符串。
		printf("Del_str_bengin_to_end_newnew  begin[%s]\n",str);
		char *pbegin,*pend,*beginstr,*allend;
		int len,len_begin,len_end;
		len_begin = strlen(begin);
		len_end = strlen(end);
		beginstr = str;
		allend = str+strlen(str);
		while(1)
		{
			len =0;
			pbegin=strstr(beginstr,begin);
			if(pbegin==NULL) break;
			pend=strstr(pbegin+len_begin,end);
			if(pend==NULL) break;
			len= pbegin-str;//strlen(str);
			*pbegin='\0';
			pend=pend+len_end;
			len =len +(allend-pend); //strlen(pend);
			strncat(str,pend,(allend-pend));
			str[len]='\0';
			beginstr= pbegin;
		}
		printf("Del_str_bengin_to_end_newnew  end[%s]\n",str);
		return 0;
		 */

		//原来的程序，在64位下有问题，已修改位安全模式.20180715
		//这里有问题，未删除删除标签前后的空格 errorerror,在sogou微信提取标题时明显
		// printf("Del_str_bengin_to_end_newnew  begin[%s]\n",str);

		char *pbegin,*pend,*beginstr,*allend;
		int len,len_begin,len_end;
		len_begin = strlen(begin);
		len_end = strlen(end);
		beginstr = str;
		allend = str+strlen(str);
		while(1)
		{
			len =0;
			pbegin=strstr(beginstr,begin);
			if(pbegin==NULL) break;
			pend=strstr(pbegin+len_begin,end);
			if(pend==NULL) break;
			len= pbegin-str;//strlen(str);
			pend = pend +len_end;
			beginstr = pbegin;
			while('\0' != *pend){
				*pbegin =*pend;
				pbegin++;
				pend++;
			}
			*pbegin= '\0';
		}
		// printf("Del_str_bengin_to_end_newnew  end[%s]\n",str);


}

/*
int write__downfile(struct LINKINFO *linkinfo,char *finename)
{

	FILE *FILE_targetfile;
	FILE_targetfile = fopen(finename, "w");
	if(FILE_targetfile )
	{
		//写文件
		fprintf(FILE_targetfile, "%s\n%s\n", linkinfo->link, linkinfo->title);
		fclose(FILE_targetfile);
	}
	else remove(finename);


}

int read__downfile(struct LINKINFO *linkinfo,char *finename)
{
	FILE   *FILE_web_linkfile;
	char *p;
	FILE_web_linkfile=fopen(finename,"r");
	if(FILE_web_linkfile==NULL)	  {  printf("Weblinkfile file can not open the file-----file=%s\n",finename); 	return 0;}
	fgets( linkinfo->link, 1000, FILE_web_linkfile ) ;
	fgets( linkinfo->title, 1000, FILE_web_linkfile ) ;
	p = linkinfo->link;
	p = p +strlen(linkinfo->link)-1;
	*p = '\0';
	p = linkinfo->title;
	p = p +strlen(linkinfo->title)-1;
	*p = '\0';
	//printf("%s\n%s\n",linkinfo->link,linkinfo->title);
	fclose(FILE_web_linkfile);
}

*/



void InitQLSH(QListSH* QL)
{
    if(QL==NULL)
        QL=(QListSH*)malloc(sizeof(QListSH));
    QL->front=NULL;
    QL->end=NULL;
}
#define iswaiting 0
#define iswroking 1
int InsertQL_tongji(struct QNodeLink* p ,int type)
{
	//web
	pthread_mutex_lock(&mymutex_num_nodelink_working);
	p->node_web->num_nodelink_working++; //web 在锁定时已经设置为1，所以在这里不用加了
	pthread_mutex_unlock(&mymutex_num_nodelink_working);
 	//p->index = p->threadinfo->LoopThread.link_insert;
	//p->threadinfo->LoopThread.link_insert++;


	if(p->layer > 1)
	{
		p->threadinfo->LoopBig.wget_depth++;
		// pthread_mutex_lock(&mymutex_wget_depth);
		//p->threadinfo->nodeWQ->LoopQueue.wget_depth++;
		//pthread_mutex_unlock(&mymutex_wget_depth);
	}
	if(iswaiting == type)
	{

		p->threadinfo->LoopBig.wget_waiting_all++;
		// pthread_mutex_lock(&mymutex_wget_waiting_all);
		//p->threadinfo->nodeWQ->LoopQueue.wget_waiting_all++;
		//pthread_mutex_unlock(&mymutex_wget_waiting_all);
	}


}
/*
int  InsertQLWaiting( struct QList* QL   ,struct QNodeLink* p)
{
	//插入等待队列
 	InsertQL_tongji( p);

	//插入低到高队列,排序
	if(QL->front==NULL)
	{
			QL->front=p;
			QL->end=p;
			p->next=NULL;
	}
	else
	{
			if( IsWeb == p->web_or_link)
			{
				//插入到头部
				p->next = QL->front;
				QL->front = p;

			}
			else
			{
					int ok =0;
					QNodeLink *pp= QL->front,*pleft=NULL;
					while(pp)
					{
							if(p->layer <= pp->layer   )
							{
									if(pp == QL->front)
									{
										//插入到头部
										p->next = pp;
										QL->front = p;
									}
									else
									{
										//插入到当前节点之前
										//p
										pleft->next = p;
										p->next = pp;
									}
									ok =1;
									break;
							}
							pleft = pp;
							pp = pp->next;
					}


					if(0 == ok)
					{
						//插入到队尾
						p->next = NULL;
						QL->end->next = p;
						QL->end = p;
					}
			}
	}





	//简单插入头部，不排序
	if(  p->layer < 1 ) //插入头部
	{
		if(QL->front==NULL)
		{
		    QL->front=p;
		    QL->end=p;
		    p->next=NULL;
		}
		else
		{
		    p->next=QL->front;
		   QL->front = p;
		}
	}
	else //插入尾部，正常方式
	{
		if(QL->front==NULL)
		{
		    QL->front=p;
		    QL->end=p;
		    p->next=NULL;
		}
		else
		{
		    p->next=NULL;
		    QL->end->next=p;
		    QL->end=p;
		}

	}

	return 1;

}
*/
/*
int  InsertQLWaiting_new( struct QNodeLink* p)
{
	if(NULL == p) return 0;
	struct THREADINFO *Threadinfo_old = p->threadinfo;
	if(NULL == Threadinfo_old->node_thread_WQ)
		Threadinfo_old->node_thread_WQ = Threadinfo_old->nodeWQ->QLThread->front;

	struct THREADINFO *Threadinfo_new =  Threadinfo_old->node_thread_WQ->Thread;




	struct QList* QL= Threadinfo_new->QLWgetWaiting;
	//插入等待队列
	p->threadinfo = Threadinfo_new;
 	InsertQL_tongji( p , iswaiting);

	pthread_mutex_lock(&mymutex_QLWgetWaiting);
	if(QL->front==NULL)
	{
	    QL->front=p;
	    QL->end=p;
	    p->next=NULL;
	}
	else
	{
	    p->next=NULL;
	    QL->end->next=p;
	    QL->end=p;
	}
	pthread_mutex_unlock(&mymutex_QLWgetWaiting);

	Threadinfo_old->node_thread_WQ = Threadinfo_old->node_thread_WQ->next;
	return 1;

}
*/
int  InsertQLWaiting_new( struct QNodeLink* p)
{
	if(NULL == p) return 0;
	//struct THREADINFO *Threadinfo_old = p->threadinfo;
	//if(NULL == Threadinfo_old->node_thread_WQ)
	//	Threadinfo_old->node_thread_WQ = Threadinfo_old->nodeWQ->QLThread->front;

	//struct THREADINFO *Threadinfo_new =  Threadinfo_old->node_thread_WQ->Thread;




	//struct QList* QL= Threadinfo_new->QLWgetWaiting;
	//插入等待队列
	//p->threadinfo = NULL;
 	InsertQL_tongji( p , iswaiting);




	//pthread_mutex_lock(&mymutex_QLWgetWaiting);
	struct QList* QL= p->threadinfo->QLWgetWaiting;
	//插入低到高队列,排序
	if(QL->front==NULL)
	{
			QL->front=p;
			QL->end=p;
			p->next=NULL;
	}
	else
	{
			if( IsWeb == p->web_or_link)
			{
				//插入到头部
				p->next = QL->front;
				QL->front = p;

			}
			else
			{
					int ok =0;
					QNodeLink *pp= QL->front,*pleft=NULL;
					while(pp)
					{
							if(p->layer <= pp->layer   )
							{
									if(pp == QL->front)
									{
										//插入到头部
										p->next = pp;
										QL->front = p;
									}
									else
									{
										//插入到当前节点之前
										//p
										pleft->next = p;
										p->next = pp;
									}
									ok =1;
									break;
							}
							pleft = pp;
							pp = pp->next;
					}


					if(0 == ok)
					{
						//插入到队尾
						p->next = NULL;
						QL->end->next = p;
						QL->end = p;
					}
			}
	}

	//pthread_mutex_unlock(&mymutex_QLWgetWaiting);

	//Threadinfo_old->node_thread_WQ = Threadinfo_old->node_thread_WQ->next;
	return 1;

}
int  InsertQLWorking( struct QList* QL   ,struct QNodeLink* p)
{
	p->threadinfo->LoopBig.wget_working_all++;
	p->threadinfo->LoopThreadSmall.wget_new_run++;
	//if(p->layer>1) p->threadinfo->LoopBig.wget_depth++;


	//简单插入头部，不排序
	if(p->layer >1) //插入头部
	{
		if(QL->front==NULL)
		{
		    QL->front=p;
		    QL->end=p;
		    p->next=NULL;
		}
		else
		{
		    p->next=QL->front;
		   QL->front = p;
		}
	}
	else //插入尾部，正常方式
	{
		if(QL->front==NULL)
		{
		    QL->front=p;
		    QL->end=p;
		    p->next=NULL;
		}
		else
		{
		    p->next=NULL;
		    QL->end->next=p;
		    QL->end=p;
		}

	}

	return 1;

}
int  InsertQLWeb(MYSQL *conn, struct QNodeWebQueue* nodeWQ ,   struct WEBINFOBASE *webinfo     ,struct LINKDATABASE *linkdatabase ,int new_or_old ,QNodeShieldWeb *domainNode )
{
	//广度遍历会造成节点数量巨大，深度遍历可以节省空间
	//插入一个任务

	////说明这个网站存在，那么要把它激活
	//	      sprintf(sql , "UPDATE `manzhua`.`web_md5` SET `activate`=1 ,`layer` =%d WHERE  `web_md5`.`md5` = CAST( 0x%s AS BINARY )   LIMIT 1" , linkinfo->layer, linkinfo->md5 );
	//先查找队列中是否有这个节点
	//重复网址插入，要处理
	if(nodeWQ->type == IsWeb && 1== new_or_old  )
	{
		/*
		//1 、 简写网址变换标准网址 http://sina.com.cn     => http://www.sina.com.cn
		char domain[100],host[200];
		if(1 == getDomain(  webinfo->link , domain)){
			if(1 == getHost(webinfo->link , host)){
				if(0 == strcmp(domain,host) ){
					//printf("InsertQLWeb  [%s]\n" , webinfo->link );
					ReplaceStr(webinfo->link , "://","://www.");
					//printf("InsertQLWeb  [%s]\n\n" , webinfo->link );
				}

			}
		}
		*/
		//2、截取://之后的网址，可以过滤掉http:// 和https://重复网址
		char md5[50];
		md5_gen_link(md5,webinfo->link);
		if(LinkNew != insert_linkmd5(conn, md5, 0,linkdatabase->layer,linkdatabase->loop,linkdatabase->download,IsWeb,webinfo->link))
		{
			//重复网址插入，要处理
			return 0;
		}
	}

	 QNodeWeb *p;
	p=(QNodeWeb*)malloc(sizeof(QNodeWeb));
	if(!p) return 0;
	p->nodeWQ = nodeWQ;
	//p的一些初始化信息

	if( nodeWQ->QLWeb->end )
		p->index = nodeWQ->QLWeb->end->index + 1;
	else
		p->index = 0;

	p->mylock = 0;
	p->download =  linkdatabase->download;//***************************************
	p->tinytype =  webinfo->tinytype;
	p->layer = linkdatabase->layer;  //**************************************
	p->webid = webinfo->webid;
	p->loop_web=  linkdatabase->loop;
	p->tm_last_download = 0;
	p->num_nodelink_working = 0;
	p->domainNode = domainNode;
	sprintf(p->domain ,"%s" , webinfo->domain);
	if(0 == strcmp(webinfo->ifout , "out"))
		p->ifout = YES;
	else
		p->ifout = NO;

	//给标准网址的link 赋值
	if(nodeWQ->type == IsWeb  ){
		p->linkkw = strcpy(nodeWQ->QLWebPub_link_p,webinfo->link);
		nodeWQ->QLWebPub_link_p = nodeWQ->QLWebPub_link_p + strlen(webinfo->link)+1;

		//p->domain = strcpy(nodeWQ->QLWebPub_web_p,webinfo->web);
		//nodeWQ->QLWebPub_web_p = nodeWQ->QLWebPub_web_p + strlen(webinfo->web)+1;

		//p->kw = NULL;
		/*
		char md5[50];
		md5_gen(md5, p->link);
		insert_linkmd5(conn, md5, 0, p->layer,p->loop_web,p->download,IsWeb,p->link);
		*/
	}
	//关键词合成的网址，link=NULL，关键词连续存储在缓存中，要采集时再合成完整链接，这样节省内存空间。用kw指向内存中地址
	else{
		//p->link = NULL;
		//p->domain= NULL;
		p->linkkw = strcpy(nodeWQ->QLWebPub_link_p,webinfo->kw);
		nodeWQ->QLWebPub_link_p = nodeWQ->QLWebPub_link_p + strlen(webinfo->kw)+1;
	}


	//低层的插入头，高层插入尾部，这样优先采集网址，提高效率
	if(nodeWQ->QLWeb->front==NULL)
	{
		nodeWQ->QLWeb->front=p;
		nodeWQ->QLWeb->end=p;
		p->next=NULL;
		p->forward=NULL;
	}
	else
	{
		int ok =0;
		QNodeWeb *pp= nodeWQ->QLWeb->front;
		while(pp)
		{
			if(p->layer <= pp->layer)
			{
				if(pp == nodeWQ->QLWeb->front)
				{
					//插入到头部
					p->next = pp;
					p->forward=NULL;
					pp->forward = p;
					nodeWQ->QLWeb->front = p;
				}
				else
				{
					//插入到当前节点之前
					//p
					p->next = pp;
					p->forward=pp->forward;

					//pp->forward
					pp->forward->next = p;

					//pp
					pp->forward  = p;
				}
				ok =1;
				break;
			}
			pp = pp->next;
		}


		if(0 == ok)
		{
			p->next = NULL;
			p->forward=nodeWQ->QLWeb->end;

			nodeWQ->QLWeb->end->next = p;

			nodeWQ->QLWeb->end = p;

		}

	}


/*
	//高层插入头部
	if(nodeWQ->QLWeb->front==NULL)
	{
		nodeWQ->QLWeb->front=p;
		nodeWQ->QLWeb->end=p;
		p->next=NULL;
		p->forward=NULL;
	}
	else
	{
		int ok =0;
		 QNodeWeb *pp= nodeWQ->QLWeb->front;
		while(pp)
		{
			if(p->layer >= pp->layer)
			{
				if(pp == nodeWQ->QLWeb->front)
				{
					p->next = pp;
					p->forward=NULL;
					pp->forward = p;
					nodeWQ->QLWeb->front = p;
					ok =1;
					break;
				}
				else
				{
					//p
					p->next = pp;
					p->forward=pp->forward;

					//pp->forward
					pp->forward->next = p;

					//pp
					pp->forward  = p;

					ok =1;
					break;
				}

			}
			pp = pp->next;
		}


		if(0 == ok)
		{
			p->next = NULL;
			p->forward=nodeWQ->QLWeb->end;

			nodeWQ->QLWeb->end->next = p;

			nodeWQ->QLWeb->end = p;

		}

	}
*/
	return 1;

}

int  IndexQLWeb(QListWeb* QL)
{	//遍历显示链表所有单元
    int i=0;
	if(QL)
	{
	    QNodeWeb*p=QL->front;

	    while(p   )
	    {
	        p->index = i;
	        i++;
	        p=p->next;
	    }
	}
	else
	{

		RecordMessage("IndexQLWeb QL=NULL",Recordworkfile,1);

	}
    return i;
}
int InsertQLTaskSHnew(QListSH* QL ,int i ,struct THREADINFO *ThreadInfo)
{
	QNodeSH *p;
	p=(QNodeSH*)malloc(sizeof(QNodeSH));


	p->index= i;
	p->numcheck= 0;
	p->working= 0;
	sprintf(p->shfilename , "%s_S_task_%d.sh" ,ThreadInfo->WgetWorkDir, i);
	FILE *FILE_targetfile;
	FILE_targetfile = fopen(p->shfilename, "w|S_IEXEC");
	if(FILE_targetfile == NULL )
	{
		printf("InsertQLTaskSHnew creat sh error [%s]\n",p->shfilename);
		return -1;
	}
	fputs(  "\n",FILE_targetfile);
	fclose(FILE_targetfile);

	//为SH中的wget队列建立链表，并分配内存
	p->QLWget =(struct QList*)malloc(sizeof(struct QList));
	InitQL(p->QLWget);   //初始化这个队列

	if(QL->front==NULL)
	{
	    QL->front=p;
	    QL->end=p;
	    p->next=NULL;
	    p->forward=NULL;
	}
	else
	{
	    p->next=NULL;
	    p->forward=QL->end;
	    QL->end->next=p;
	    QL->end=p;
	}

	return 1;
}
/*
int add_nodeSH(struct THREADINFO *ThreadInfo)
{
	//针对QLTaskSH队列增加一个节点
	if(ThreadInfo->nodeWQ->num_sh_public > 0)
	{
		ThreadInfo->nodeWQ->num_sh_public--;
		InsertQLTaskSHnew(ThreadInfo->QLTaskSH , ThreadInfo->QLTaskSH->end->index+1, ThreadInfo);
		ThreadInfo->num_sh++;
	}


	return 0;
}


int clear_nodeSH(struct THREADINFO *ThreadInfo)
{

	QNodeSH *p ,*pleft;
	p = ThreadInfo->QLTaskSH->front;
	while(p)
	{
		if(p->index > ThreadInfo->num_sh)
		{
			pleft->next = p->next;
			free(p);
			p = pleft;
		}
		pleft = p;
		p = p->next;
	}


	return 0;
}
*/
int display_error(struct THREADINFO *ThreadInfo,QNodeLink*p ,int pos)
{

		char buf[4000];
		sprintf(buf,"---%d---  web_index=%2d  loop=%d num_nodelink_working=%3d   WQ=%d  download=%d    thread=%d    loop=%3d/%d\n link[%d][%s]\n web [%d][%s]\n",
				pos,
				ThreadInfo->node_web_new->index,
				p->node_web->loop_web,
				p->node_web->num_nodelink_working,
				ThreadInfo->nodeWQ->index,
				p->node_web->download,
				ThreadInfo->myid,
				ThreadInfo->loop_thread,
				ThreadInfo->nodeWQ->loop_WQ,
				p->layer,p->linknew,p->node_web->layer,p->node_web->linkkw
			 );
		Recordwork(buf,Recordworkfile);



}
QNodeLink*  DeleteQLfront(struct QList* QL  )
{
	//删除队列的第一个节点
	//pthread_mutex_lock(&mymutex_QLWgetWaiting);
	QNodeLink*p=QL->front;;
	if(p == NULL) return NULL ;


	//删除头节点
	if(QL->front->next==NULL)
	{
	    QL->front=NULL;
	    QL->end=NULL;
	}
	else
	{
		QL->front = p->next;
	}
	p->next = NULL;
	//pthread_mutex_unlock(&mymutex_QLWgetWaiting);
	return p;




}
QNodeLink*  DeleteQLfront_QLWgetSH(struct QList* QL  )
{
	//删除队列的第一个节点

	QNodeLink*p=QL->front;;
	if(p == NULL) return NULL ;


	//删除头节点
	if(QL->front->next==NULL)
	{
	    QL->front=NULL;
	    QL->end=NULL;
	}
	else
	{
		QL->front = p->next;
	}
	//p->next = NULL;
	return p;




}
/*
int DeleteQLNode_update(QNodeLink* p)
{

	p->node_web->num_nodelink_working--;; //web 在锁定时已经设置为1，所以在这里不用加了
	p->threadinfo->LoopBig.wget_waiting_all--;
	if(p->layer > 1) p->threadinfo->LoopBig.wget_depth--;

}
*/
/*
int  update_some(QNodeLink*p)
{

	if(p->layer > 1)  p->threadinfo->LoopBig.wget_depth--;

	//bigloop大于1时，可能会新添加一些网址，这些网址默认值是0，如果采集后加1，而都列却是2，就少了，所以网址采集后要和圈数同步
	p->node_web->num_nodelink_working--;
	if( 0 == p->node_web->num_nodelink_working)
	{
		unlock_web_md5 ( p->node_web, p->threadinfo->loop_thread ,1);
	}

}
*/
int  freeQNodeLink_UpdateBase(QNodeLink*p)
{
	//删除一个节点需要更新一些信息
	if(p->layer > 1)
	{
		p->threadinfo->LoopBig.wget_depth--;
		//pthread_mutex_lock(&mymutex_wget_depth);
		//p->threadinfo->nodeWQ->LoopQueue.wget_depth--;
		//pthread_mutex_unlock(&mymutex_wget_depth);
	}

	pthread_mutex_lock(&mymutex_num_nodelink_working);
	p->node_web->num_nodelink_working--;
	pthread_mutex_unlock(&mymutex_num_nodelink_working);
	if( 0 == p->node_web->num_nodelink_working)
	{
		unlock_web_md5 ( p->node_web, p->threadinfo->loop_thread ,1);
		//删除cookie文件
		if(2<1 &&  p->threadinfo->nodeWQ->type == IsWeiXin  )
		{
			char cookie_file[200];
			get_cookie_filename(p->md5_father, p->threadinfo->WgetWorkDir, cookie_file);
			remove(cookie_file);
		}
	}

}

int DeleteQLWget_QLWgetWaiting(QNodeLink*p)
{

	//释放节点
	freeQNodeLink_UpdateBase( p);
	freeQNodeLink(p);

	return 0;
}

int DeleteQLWget_QLWgetSH(MYSQL *conn, struct QList* QL ,struct THREADINFO *ThreadInfo )
{

	//移除sh中wget队列中的头节点，这些节点已经采集过的。
	if(QL->front){
		QNodeLink*p=QL->front;
		//工作中的wget更新
		ThreadInfo->LoopBig.wget_working_all--;
		if( IsWeb == p->web_or_link)
			ThreadInfo->nodeWQ->num_web_working--;

		//删除 out_file
		if(2<1 && IsWeiXin == p->threadinfo->nodeWQ->type  )
		{
			if( IsWeb == p->web_or_link){
			}
			else{
				char out_file[200];
				get_out_filename(p->md5,ThreadInfo->WgetWorkDir , out_file );
				unlink(out_file);
			}
		}


		 //链接采集次数更行



		if(p->download_link < Download_OKInit)  ThreadInfo->LoopThread.link_bad++;
		if(p->web_or_link == IsWeb)  p->node_web->download = p->download_database;


		//释放更新代理服务器
		if( p->node_proxy) //p->threadinfo->nodeWQ->index_proxy > -1 &&  p->web_or_link == IsWeb &&
		{
			 int index_proxy =  p->threadinfo->nodeWQ->index_proxy;
			// printf("free  proxy_index=%d              download_link=%d     parselinknum=%d \n" , p->node_proxy->index ,p->download_link ,p->parselinknum );

			 if(p->parselinknum > 0)
			 	p->node_proxy->good[index_proxy]--;// = proxy_free;
			 else
		 	{
		 		//ThreadInfo->node_proxy = find_proxy( QLProxy , p->node_proxy , ThreadInfo->nodeWQ->index_proxy);//移动到安全地带
		 		//printf("index_proxy=%d\n",index_proxy);
		 		p->node_proxy->good[index_proxy] = proxy_error;
				//printf("--------------------------------proxy_error %d\n",p->node_proxy->index);
		 	}
		}

		// if(  node_web->num_nodelink_working <  1) display_error( ThreadInfo,  p, 1);
	 	unlock_link_md5(conn,   p);
		p = DeleteQLfront_QLWgetSH( QL );
		freeQNodeLink_UpdateBase(p);
		freeQNodeLink(p);

		//给下一个WGET赋值开始下载时间
		if(QL->front)	update_download_tm(QL->front);
	}
	return 0;

}

int DeleteQLWebNode( QListWeb* QL , QNodeWeb*p_delete )
{
	//删除一个任务

	if(QL->front == p_delete) //删除是头
	{
		if(QL->end ==  p_delete) //只有一个节点
		{
		    QL->front=NULL;
		    QL->end=NULL;
			free(p_delete);
			p_delete = NULL;
			return 1;
		}
		else
		{
			QL->front  = p_delete->next;
			free(p_delete->linkkw);p_delete->linkkw = NULL;
			//free(p_delete->domain);p_delete->domain = NULL;
			free(p_delete);	 p_delete = NULL;
			return 1;
		}

	}
	else
	{
		QNodeWeb*p;
		p=QL->front;
		while(p   )
		{
		    if(p->next == p_delete)
			{
				if(QL->end == p_delete)
				{
					QL->end =p;
				}
				p->next = p_delete->next;
				free(p_delete->linkkw); p_delete->linkkw = NULL;
				//free(p_delete->domain); p_delete->domain = NULL;
				free(p_delete);  p_delete = NULL;
				return 1;
			}

		    p=p->next;
		}

	}
	return 0;

}
int DeleteQLWeb( QListWeb* QL   )
{
	//删除所有网址节点
	QNodeWeb*nodeweb;
	while(QL->front!=NULL)
	{
		nodeweb=QL->front;
		if(QL->front->next==NULL)
		{
		    QL->front=NULL;
		    QL->end=NULL;
		}
		else
		{
		    QL->front=nodeweb->next;
		}
		//printf("%d [%s]\n",nodeweb->index,nodeweb->link);
		//这三个变量的存储空间是统一释放的
		nodeweb->linkkw = NULL;
		//nodeweb->domain = NULL;
		//nodeweb->kw = NULL;
		nodeweb->nodeWQ = NULL;
		nodeweb->next = NULL;
		nodeweb->forward =NULL;

		free(nodeweb);
		nodeweb = NULL;
	}
	free(QL);
	QL= NULL;
	return 0;

}
int DeleteQL( struct QList* QL   )
{
	//删除一个任务
	QNodeLink*p;
	while(QL->front!=NULL)
	{
		p=QL->front;
		if(QL->front->next==NULL)
		{
		    QL->front=NULL;
		    QL->end=NULL;
		}
		else
		{
		    QL->front=p->next;
		}
		freeQNodeLink(p);

	}
	return 0;

}
int DeleteQLAll( struct QList* QL   )
{
	//删除一个任务
	QNodeLink*p;
	while(QL->front!=NULL)
	{
		p=QL->front;
		if(QL->front->next==NULL)
		{
		    QL->front=NULL;
		    QL->end=NULL;
		}
		else
		{
		    QL->front=p->next;
		}
		freeQNodeLink(p);

	}
	free(QL);
	QL = NULL;
	return 0;

}

int DeleteQLSHAll( QListSH* QL   )
{
	//删除一个任务
	QNodeSH *p;
	QNodeLink* pp;
	while(QL->front)
	{
		p=QL->front;
		if(QL->front->next==NULL)
		{
		    QL->front=NULL;
		    QL->end=NULL;
		}
		else
		{
		    QL->front=p->next;
		}


		while(p->QLWget->front)
		{
			pp=p->QLWget->front;
			if(p->QLWget->front->next==NULL)
			{
			    p->QLWget->front=NULL;
			    p->QLWget->end=NULL;
			}
			else
			{
			    p->QLWget->front=pp->next;
			}
			freeQNodeLink(pp);
		}
		free(p->QLWget);
		p->QLWget = NULL;

		free(p);
		p=NULL;

	}
	free(QL);
	QL = NULL;
	return 0;

}


int  CountQL(struct QList* QL)
{	//遍历显示链表所有单元
    int i=0;
    QNodeLink* p;
    p=QL->front;
    while(p   )
    {
        //printf("%d\t",p->link);
        i++;
        p=p->next;
    }
    return i;
}
/*
int CountQLAll()
{
	int i;
	int num =0;
	for(i = 0 ; i <num_QLWgetWaitingError;i++)
	{

		num = num + CountQL(QLWgetWaitingError[i]  );
	}
	return num;

}
*/



//int MaxQLNum=10;
int iaskDirFileNum = 10;
//char *wgetworkingnumdir="/dev/shm/";


void make_targetdir_name(struct THREADINFO *ThreadInfo)
{

	unsigned int now_tm=time((time_t *) NULL);
	char tmp[200],tmpdir[200];
	sprintf(tmpdir,"%s%d/",Targetdir,ThreadInfo->myid);
	//sprintf(tmp,"iask%u.%d.%d.%u/",now_tm,ThreadInfo->myid,ThreadInfo->webid,ThreadInfo->linkhash);
	ThreadInfo->CreatDir.index++;
	sprintf(tmp,"iask%d.%d.%d.%d/",now_tm,ThreadInfo->myid,ThreadInfo->loop_thread,ThreadInfo->CreatDir.index);
	sprintf(ThreadInfo->CreatDir._targetdir,"%s_%s", tmpdir,tmp);
	sprintf(ThreadInfo->CreatDir.targetdir,"%s%s",tmpdir,tmp);
	mkdir(ThreadInfo->CreatDir._targetdir,0755);

	ThreadInfo->CreatDir.tm_lastmkdir  = now_tm;
	ThreadInfo->CreatDir.filenum= 0;
}
int do_targetdir(struct THREADINFO *ThreadInfo)
{

	int tm=time((time_t *) NULL);
	if(ThreadInfo->CreatDir.filenum > iaskDirFileNum || ThreadInfo->CreatDir.filenum > 0 && tm - ThreadInfo->CreatDir.tm_lastmkdir > 180 ) //文件夹中文件数量大于10或文件夹中有文件而且时间超过180秒都合成目录传递，并生成新目录
	{
		rename(ThreadInfo->CreatDir._targetdir ,  ThreadInfo->CreatDir.targetdir);

		//建立信息的目录
		make_targetdir_name(ThreadInfo);
		return 1;
	}

	return 0;
}
//-------------------------------------------------------
//下载一个链接的内容和某个字符串比较
//------------------------------------------------------
int  checkRemoteStr(char *link ,char *str){
	// -1 下载失败
	// 0 不相等
	// 1 相等
	HCkHttp http;
	BOOL success;
	const char *html;
	http = CkHttp_Create();

	//  Any string unlocks the component for the 1st 30-days.
	success = CkHttp_UnlockComponent(http,"RANZENHttp_EsyVx7eaZD37");
	if (success != TRUE) {
		printf("%s\n",CkHttp_lastErrorText(http));
		CkHttp_Dispose(http);
		return -1;
	}

	//  Send the HTTP GET and return the content in a string.
	html = CkHttp_quickGetStr(http,link);
	int myreturn;
	if(html ) {
		if(0 == strcmp(html,str)){
			//printf("checkRemoteStr[%s]  %s\n",html ,link);
			myreturn =1;
		}
		else{
			//printf("checkRemoteStr[%s]  %s\n",html ,link);
			myreturn =0;
		}
	}
	//没下载成功
	else{
		//printf("checkRemoteStr[bad]  %s\n",link);
		myreturn = -1;
	}
	CkHttp_Dispose(http);
	return myreturn;
}
//-------------------------------------------------------
//检查汇总服务器连接的md5,看看是否有服务器已经采集了。
//------------------------------------------------------
int checkLinkCenter(char *md5){
	if(1 == IfCheckCenter){
		char link[200];
		sprintf(link,"%s?md5=%s" ,CheckCenterLink, md5 );
		return checkRemoteStr(link , "1");
	}
	else
		return 0;
}
int do_new_file(  QNodeLink* node_now,struct THREADINFO *ThreadInfo , char *sourcehtml){
		FILE *FILE_targetfile;
		char targetfile[200] ,_targetfile[200],tmp[200],title[2000] ;

		//去下载这个链接，并且把链接和标题放到源码的首页
		title[0]= '\0';
		if(node_now->titlenew){
				//sprintf(title,"%s",now_linkinfo->titlenew);
				if(strlen(node_now->titlenew)>2){   //处理标题
						Clean_special_str(node_now->titlenew);
						Del_other_not_blank(node_now->titlenew);
						Del_null_begin_and_end(node_now->titlenew);
				}
				sprintf(title,"%s",node_now->titlenew);
		}
		//第三次检查链接
		if( 0 == checkLinkThird(node_now->linknew) )
			return 0;
		/*
		//链接最后屏蔽检查 ,没必要了。
		if( HAVE == QLShield_PublicLink_Check(QLShieldWeb , Public_Shield_EndLink , node_now->linknew)  )
			return 0;
		*/
		//有个漏网之鱼，在检查estarlink_end_good时，如果不是在末级，时不检查的，那中间层也会有新信息产生，所以必须在这里过滤
		if( node_now->layer > 0  &&   NOTHAVE == QLShield_Domain_Check(QLShieldWeb , node_now->node_web->domainNode,  node_now->linknew ,estarlink_end_good) )
			return 0;

		//标题检查
		if( 0 == Judge_Title(title) )
			return 0;
		/*
		//检查汇总连接中心，应该在换个地方
		if( HAVE == checkLinkCenter(node_now->md5)  )
			return 0;
		*/
		/*
		//这个地方应该可以免检了，前边提取链接时已经检查过了，最多也就检查一下，底层链接情况
		//出域的网站检查数据库屏蔽网址和链接，这个地方比如微博等需要免检
		if( 	YES == node_now->node_web->ifout
			&& (IsWeb == node_now->node_web->nodeWQ->type || IsSearch  == node_now->node_web->nodeWQ->type)
			&&  HAVE ==  CheckDBShieldAndQLShieldWeb(ThreadInfo->conn , node_now->linknew)
			//&& NO    ==  QLShield_Domain_CheckAll(QLShieldWeb   , node_now->linknew  , 0 )
		)
			return 0;

		*/

		//3.增加文件头信息包括标题和链接还有三个空行
		// 1.合成目标文件名 iask_41_1.htm-2   iask_5_16.htm-2.txt
		sprintf(tmp  ,"iask_%d_%d.htm-2",  ThreadInfo->myid ,ThreadInfo->LoopBig .link_okwrited);//Str2int_map(node_now->linknew));// now_linkinfo->linkhash
		sprintf(_targetfile,"%s_%s", ThreadInfo->CreatDir._targetdir , tmp);
		sprintf(targetfile  ,"%s%s",  ThreadInfo->CreatDir._targetdir ,tmp);
		FILE_targetfile = fopen(targetfile, "w");     //20140526
		if(FILE_targetfile )	{
				//写文件
				fprintf(FILE_targetfile, "%s\n%s\n%d\n\n\n\n%s", node_now->linknew,title, node_now->node_web->webid,sourcehtml);
				fclose(FILE_targetfile);

				//转码
				// iii=NewNewChangeCharset(_targetfile,targetfile,now_linkinfo->link, ThreadInfo->myid,Encadir );//20140526
				ThreadInfo->LoopThread.link_okwrited++;
				ThreadInfo->LoopBig .link_okwrited++;
				ThreadInfo->LoopBig .link_okwrited_total++;
				ThreadInfo->CreatDir.filenum++;
				//如果有新信息了，而且原来数据库中没有记录，那么更新一下，避免归入无信息网站。还未设计好
		}
		else
				remove(_targetfile);

		return 1;
}



int composite_url(char *head,char *bottom ,int what)
{
	//合成物理链接,最后合成信息要放到bottom中
	char buf[1000];
	int aaa= 0,lead_len = strlen(head) ;
	if(( strstr(bottom,"http://") ||  strstr(bottom,"https://") )  && bottom[0] == 'h')   // http://epaper.oeeee.com =>http://epaper.nddaily.com/A
	{ 	}
	else if( strstr(bottom,"http:./") && bottom[0] == 'h')   //http://auto.online.sh.cn/ => http:./node/index.htm
	{
		if(head[lead_len-1] == '/')  //http://auto.online.sh.cn/
			ReplaceStr(bottom ,"http:./", head);

		else  //http://auto.online.sh.cn
			ReplaceStr(bottom ,"http:.", head);
	}
	else
	{
		//比较复杂的详细分析
		char headbak[501],headbakbuf[501] ,bottombak[501],*p_bottombak,*p_headbak,*pp;

		sprintf(headbak,"%s",head);
		sprintf(headbakbuf,"%s",head);
		//if(headbak[lead_len-1] == '/')  headbak[lead_len-1] ='\0';

		sprintf(bottombak,"%s", bottom);
		//p_bottombak = bottombak;
		//if(*p_bottombak == '/' ) p_bottombak++;


		int i=0,num=0 ;
		char *buf,*p[100];

		buf=strstr(headbakbuf, "://");
		if(buf &&  strlen(buf) > 3)
			buf = buf+3;//跳过http://
		else
		{
			printf("errorhead [%s]\n" , head);
			return 0;
		}

		//buf = index(headbakbuf, '/');
		//buf = buf +2;          //跳过http://
		while((p[i]=strtok(buf,"/"))!=NULL)
		{
			i++;
			buf=NULL;
			if(i > 98)
			{
				printf("error i=%d\n" , i);
				return 0;
			}
		}
		num =i;

		/*
		if(buf[strlen(buf) - 1] == '/') buf[strlen(buf) - 1] = '\0';
		p[i] = buf;
		i++;
		p[i]=index(buf,'/');
		while(p[i]  )
		{
			*p[i] = '\0';
			 p[i]++;
			 i++;
			 p[i]=index(buf,'/');
		}
		num =i;
		//for(i = 0; i<num;i++) printf("%d[%s]\n",num,p[i]);
		*/


		if(num == 0)
		{
			aaa= 2;
		}
		else if(num ==1 )
		{
			if(head[lead_len-1] != '/' && bottom[0] != '/')    //window.location.href = "cif/html";     http://cif.mofcom.gov.cn   //<script>window.location.href='2012/08/01/01/default.htm'</script>   http://203.86.76.53
				sprintf(bottom,"%s/%s" , headbak, bottombak);
			else if(head[lead_len-1] == '/' && bottom[0] != '/'  || head[lead_len-1] != '/' && bottom[0] == '/' )
				sprintf(bottom,"%s%s" , headbak, bottombak);
			else
			{
				p_bottombak = bottombak;
				p_bottombak++;
				sprintf(bottom,"%s%s" , headbak, p_bottombak);
			}
		}
		else //num > 1
		{

			if(head[lead_len-1] == '/' && bottom[0] != '/')  //http://www.sinoins.com/news/     location="list.html"
				sprintf(bottom,"%s/%s" , headbak, bottombak);
			else if(head[lead_len-1] != '/' && bottom[0] != '/'   )
			{

				if(  index(p[num -1] , '.'))
				{
				//window_location_href [http://list.html] [http://www.sinoins.com/news/index.html]
					//<html><script language=vbscript>location="list.html"</script></html>   //http://www.sinoins.com/news/index.html       =>http://www.sinoins.com/news/list.html
					//<script type="text/javascript">location="index.html";</script>         //http://bbs.house365.com/main.php  还为处理   =>http://bbs.house365.com/index.html
					p_headbak = rindex(headbak,'/');
					*(p_headbak+1) = '\0';
					sprintf(bottom,"%s%s" , headbak, bottombak);
				}
				else  //http://www.lasa-eveningnews.com.cn/epaper   <script>window.location.href='2012/08/02/01/default.htm'</script>
					sprintf(bottom,"%s/%s" , headbak, bottombak);

			}
			else
			{
				aaa= 1;
				//sprintf(buf,"aaa[%s]   [%s]\n" ,head, bottom);

			}
		}

	}


	//sprintf(buf,"%d [%d] [%s]   [%s]\n",aaa,what,head, bottom );
	//NewRecordwork(buf,ErrorFile);
	return 1;
}

int get_refresh(MYSQL *conn,struct QNodeLink *node_now ,char *sourcehtml ,struct LINKTITLE *linktitle ,char *p_head)
{
		int len;
		char *begin,*begin2,*begin3,*end,*end2 , *p_end;
		//检查刷新、转向链接
		//<META HTTP-EQUIV="REFRESH" CONTENT="0; URL=http://paper.ctn1986.com/fzb/paperindex.htm">
		//<meta http-equiv="Refresh" content="0;url=http:./node/index.htm">
		//<meta http-equiv="Refresh" content="60; url=hq.jsp" >
		//printf("aaaaaaaaaa\n%s\n",sourcehtml);
		//<meta http-equiv="refresh" content="5;URL=http://www.people.com.cn/" />
		//<meta http-equiv="refresh" content="300; url=http://3g.163.com/x/"/>
		begin2 = strstr(sourcehtml , "http-equiv=\"REFRESH\"");
		if(begin2 == NULL)   begin2 = strstr(sourcehtml , "http-equiv=\"Refresh\"");
		if(begin2 == NULL)   begin2 = strstr(sourcehtml , "http-equiv=\"refresh\""); //<meta http-equiv="refresh" content="0;URL=http://epaper.nddaily.com/A">   http://epaper.oeeee.com
		if(begin2 == NULL)   begin2 = strstr(sourcehtml , "HTTP-EQUIV=\"REFRESH\"");//<META HTTP-EQUIV="REFRESH" CONTENT="0; URL=html/2015-07/03/node_5.htm">  http://sjzrb.sjzdaily.com.cn/

		if(begin2 &&  begin2<p_head)
		{
			/*
			end = strstr(begin2,"\">");
			end2 = strstr(begin2,"\" >");
			if(end && end2 && end2 < end)  end = end2;
			*/
			end2 = index(begin2 ,'>');
			if(end2  && end2-begin2 < 200)
			{
				begin3 = begin2;
				begin2 = strstr(begin3 , "URL=");
				if(begin2 == NULL || begin2 > end2) begin2 = strstr(begin3 , "url=");

				if(begin2 && begin2 < end2)
				{
					begin2 = begin2 + 4;
					if(begin2<end2)
					{
						end = index(begin2 ,'"');
						if(end== NULL || end>end2 ||  end-begin2 > 4999)  return 0;
						strncpy(linktitle->link,begin2 ,end-begin2);
						linktitle->link[end-begin2] = '\0';

						Del_other(linktitle->link);
						convert_unicode(linktitle->link);
						if( strcmp(linktitle->link ,node_now->linknew) == 0) return 0;
						composite_url(node_now->linknew,linktitle->link , 0 );

						sprintf(linktitle->title,"this is refresh");
						//len = strlen(linktitle->link );
						//if(checkLinkFirst(linktitle->link  , len) <1 ||  checkLinkSecond(conn,QLShieldWeb,linktitle->link) <1)    return 0;
						//由于--convert-links  会把文件名作为链接替换下载链接，必须加以过滤
						if(strstr(linktitle->link  , node_now->threadinfo->_son_wget_info)  )     return 0;

						//linkinfo->layer =   now_linkinfo->layer;
					}
					else return 0;
				}
				else return 0;
			}
			else return 0;
		}
		else return 0;
		//printf("[%s]\n",linktitle->link);
	return 1;
}
/*
int get_frame(struct LINKINFO *now_linkinfo ,  struct LINKINFO *linkinfo ,char *sourcehtml ,struct LINKTITLE *linktitle ,char *p_head)
{
		int len;
		//char *begin,*begin2,*begin3,*end,*end2 , *p_end;
		char *p_frame,*framebegin,*frameend,*httpbegin,*httpend;

		//检查frame框架链接转向
		//<frame name="main" src="http://digitalpaper.stdaily.com:81/http_www.kjrb.com/kjrb/paperindex.htm">
		//<iframe src="http://www.51.index-gg.asp" marginwidth="0" marginheight="0" scrolling="no" frameborder="0" style="width:760px;height:108px;">
		p_frame=sourcehtml;
		framebegin  = strstr(p_frame , "<frame ");
		if(framebegin == NULL)   framebegin = strstr(p_frame , "<iframe ");

		if(framebegin)
		{
			p_frame = framebegin + 7;
			frameend = strstr(p_frame,">");
			if(frameend  && frameend-framebegin < 200)
			{
				httpbegin = strstr(p_frame , "src=\"");
				if(httpbegin && httpbegin < frameend)
				{
					httpbegin = httpbegin + 5;
					httpend = strstr(httpbegin,"\"");
					if(httpend && httpend  < frameend  && httpend-httpbegin > 0)
					{
						if(httpend-httpbegin> 4999) return 0;
						strncpy(linktitle->link,httpbegin ,httpend-httpbegin);
						linktitle->link[httpend-httpbegin] = '\0';
						Del_other(linktitle->link);
						if( strcmp(linktitle->link ,now_linkinfo->linknew) == 0) return 0;
						if( strstr(linktitle->link ,"http:") == NULL) return 0;
						if(MyDebug > 0)
						{
							*frameend = '\0';
							printf("this is iframe[%s]\n[%s]\n[%s]\n\n",linktitle->link,now_linkinfo->linknew,framebegin);
							*frameend = '>';
						}
						sprintf(linktitle->title,"this is iframe");

						len = strlen(linktitle->link );
						if(checkLinkFirst(linktitle->link  , len) <1 )    return 0;
						linkinfo->layer =  now_linkinfo->layer;
						//frame = 0; //只取一个框架
					}
					else return 0;

				}
				else return 0;
			}
			else return 0;
		}
		else {
		//frame = 0;
		return 0;}


	return 1;
}
*/
int get_window_location_href(MYSQL *conn,struct QNodeLink *node_now   ,char *sourcehtml ,struct LINKTITLE *linktitle ,char *p_head)
{
		int len;
		//char *begin,*begin2,*begin3,*end,*end2 , *p_end,*httpbegin,*httpend;

		char *p_window_location_href ,*end_window_location_href,*begin_window_location_href,*httpbegin,*httpend;

		p_window_location_href = sourcehtml;
		//检查window.location.href
		int aaa=0; //"  1是'
		//window_location_href  = 0; //只取一次

		//window.location.href = "cif/html";     http://cif.mofcom.gov.cn
		begin_window_location_href  = strstr(p_window_location_href , "window.location.href = \"");
		len = strlen("window.location.href = \"");

		//window.location.href="http://opinion.cntv.cn/";
		if(begin_window_location_href == NULL)
		{
			begin_window_location_href = strstr(p_window_location_href , "window.location.href=\"");
			len = strlen("window.location.href=\"");
		}

		//<script>window.location.href='2012/08/01/01/default.htm'</script>   http://203.86.76.53居然没有head标记
		if(begin_window_location_href == NULL)
		{
			begin_window_location_href = strstr(p_window_location_href , "window.location.href='");
			len = strlen("window.location.href='");
			aaa=1;
		}

		if(begin_window_location_href == NULL)
		{
			begin_window_location_href = strstr(p_window_location_href , "window.location.href = '");
			len = strlen("window.location.href = '");
			aaa=1;
		}
		//<script type="text/javascript">location="index.html";</script>         //http://bbs.house365.com/main.php  还为处理   =>http://bbs.house365.com/index.html
		//<html><script language=vbscript>location="list.html"</script></html>   //http://www.sinoins.com/news/index.html       =>http://www.sinoins.com/news/list.html
		if(begin_window_location_href == NULL )   //&&  sourcehtml_len < 1024
		{
			begin_window_location_href = strstr(p_window_location_href , "location=\"");
			len = strlen("location=\"");
			aaa=0;
		}
		/*   20160823
			http://epaper.anhuinews.com/
			<script>
			hrefValue = window.location.href

			if(hrefValue=='http://www.ahfzb.com/'){location.href="http://www.ahfzb.com/html/ahfzb.shtml"}else
			if(hrefValue=='http://epaper.crec4.com/'){location.href="http://epaper.crec4.com/html/tdjs.shtml"}else
			{location.href="http://epaper.anhuinews.com/html"}</script>
		*/
		if(begin_window_location_href == NULL )   //&&  sourcehtml_len < 1024
		{
			begin_window_location_href = strstr(p_window_location_href , "location.href=\"");
			len = strlen("location.href=\"");
			aaa=0;
			//if(begin_window_location_href) printf("get_window_location_href 222222222222222222222222222222222    %d\n",begin_window_location_href - p_head);
		}




		if(begin_window_location_href   && begin_window_location_href < p_head)
		{

			begin_window_location_href = begin_window_location_href + len;
			if( aaa < 1)
				end_window_location_href = strstr(begin_window_location_href,"\"");
			else
				end_window_location_href = strstr(begin_window_location_href,"'");

			if(end_window_location_href  && end_window_location_href-begin_window_location_href < 200   && end_window_location_href < p_head)
			{
				httpbegin = begin_window_location_href;
				httpend = end_window_location_href;

				if(httpend-httpbegin> 4999) return 0;
				strncpy(linktitle->link,httpbegin ,httpend-httpbegin);
				linktitle->link[httpend-httpbegin] = '\0';

				Del_other(linktitle->link);
				convert_unicode(linktitle->link);
				if( strcmp(linktitle->link ,node_now->linknew) == 0)  return 0;
				if(linktitle->link[strlen(linktitle->link) - 1] == '_' || linktitle->link[strlen(linktitle->link) - 1] == '=' || linktitle->link[strlen(linktitle->link) - 1] == '-' )  return 0;

				composite_url(node_now->linknew,linktitle->link ,2);
				/*
				if( strstr(linktitle->link ,"http:") == NULL)
				{
					char tmplink[501] ,tmplink2[501];
					sprintf(tmplink,"%s",now_linkinfo->link);
					sprintf(tmplink2,"%s", linktitle->link);
					if(tmplink[strlen(tmplink)-1] == '/') tmplink[strlen(tmplink)-1] ='\0';
					if(tmplink2[0] == '/' )
						sprintf(linktitle->link ,"%s%s" , tmplink, tmplink2);
					else
						sprintf(linktitle->link ,"%s/%s" , tmplink, tmplink2);
				}*/
				sprintf(linktitle->title,"window_location_href");

				//len = strlen(linktitle->link );
				//if(checkLinkFirst(linktitle->link  , len) <1 ||  checkLinkSecond(conn,QLShieldWeb,linktitle->link) <1)     return 0;
				//由于--convert-links  会把文件名作为链接替换下载链接，必须加以过滤
				if(strstr(linktitle->link  , node_now->threadinfo->_son_wget_info)  )     return 0;
				//printf("window_location_href [%s] [%s]\n" , linktitle->link,now_linkinfo->link );
				//linkinfo->layer =  now_linkinfo->layer;
			}
			else  return 0;
		}
		else {/*window_location_href = 0;*/ return 0; }


	return 1;
}
/*
int nodelink_inherit(struct QNodeLink *node_src,struct QNodeLink *node_new ,int layer)
{
		node_new->loop_link= 0;//在这个加时最合理的
		node_new->web_or_link= IsLink;
		if(layer<0)
			node_new->layer = 0;
		else
			node_new->layer = layer;
		node_new->node_web= node_src->node_web;
		node_new->node_proxy = NULL;//node_src->node_proxy;
		node_new->threadinfo= node_src->threadinfo;

		node_new->download_database = Download_OKInit;
		node_new->download_link =         Download_OKInit; //由于是第一圈，暂时先认为他是个好链接
}
*/
struct QNodeLink* create_new_node_link(struct THREADINFO *ThreadInfo,QNodeWeb *node_web ,int layer ,int web_or_link ,int download_database ,int  size_link , int size_title ,int  loop_link_father)
{
	QNodeLink* node_link;
	node_link=(QNodeLink*)malloc(sizeof(QNodeLink));

	node_link->SNUID[0] = '\0';
	node_link->linknew = NULL;
	node_link->titlenew = NULL;
	node_link->node_web= node_web;//ok
	node_link->node_proxy =  NULL; //ok
	node_link->threadinfo= ThreadInfo;//ok
	node_link->size_last = 0;
	node_link->web_or_link = web_or_link;
	node_link->loop_link= 0;
	node_link->loop_link_father = loop_link_father;
	node_link->ifdownloaded=0;
	node_link->index = ThreadInfo->node_link_index;
	ThreadInfo->node_link_index++;
	if(layer<0)
		node_link->layer = 0;
	else
		node_link->layer = layer;

	node_link->download_database = download_database;
	node_link->download_link =         Download_OKInit; //由于是第一圈，暂时先认为他是个好链接



	node_link->begin_wget_download_tm = 0;
	node_link->parselinknum = 0;
	//node_link->num_download= 0;
	//node_link->numcheck=0;



	//网页处理
	if(IsWeb == node_link->web_or_link)
	{
		lock_web_md5 (  node_link, ThreadInfo->nodeWQ,node_link->node_web) ;
	}
	else
	{
		int other;
		if(2<1 && IsWeiXin == node_link->threadinfo->nodeWQ->type)
			other = 100;
		else
			other = 1;
		node_link->linknew= (char *)malloc(size_link+1+other);
		node_link->linknew[0] = '\0';

		if(0 == size_title)
			node_link->titlenew = NULL;
		else
		{
			node_link->titlenew= (char *)malloc(size_title+1+1);
		      node_link->titlenew[0] = '\0';
		}
	}


	return node_link;


}

QNodeLink* check_a_nodeLink(MYSQL *conn,QNodeLink* nodelink )
{
		//,struct QList *QLWgetWaiting ,struct THREADINFO *ThreadInfo
		//寻找可以下载的节点，若节点不符合要求，就删除，符合条件移出
		int ifdownload=0 ;

		nodelink->query_return  = lock_link_md5( conn, nodelink->threadinfo, nodelink );
		if(nodelink->query_return > Link_Unlock)
		{
				if(nodelink->layer == 0 )  //末级
				{
						if(nodelink->query_return == 2)  //新链接
						{
								//printf("[%d][%s]\n[%d][%s]\n\n",nodelink->layer, nodelink->linknew,node_now->layer, node_now->linknew);
								//if(  nodelink->node_web->loop_web > 0 ) //只有网址是第二次采集新链接才入库	//
								if(nodelink->loop_link_father > 1 || 1 == nodelink->threadinfo->nodeWQ->always_download || IsWeiXin == nodelink->threadinfo->nodeWQ->type )// nodelink->node_web->loop_web >0)
									ifdownload=1;
								else
									ifdownload=0;
						}
						else
						{
							ifdownload=0;
							printf("adddddddddddddddddddddddddddddddd\n"); //没有这种可能性
						}
				}
				else //多级
				{
						//对于取两层以上的链接，如果是新链接，则必须下载，如果是老链接，那么要判断这个链接是正文，还是频道，正文就不下载了
						if(nodelink->query_return == 2)  //新链接，这有可能是新正文，所以必须下载
						{

							if(link_is_info_or_channel(conn,nodelink->linknew) != IsInfo)
								ifdownload  = 1;
							else //是信息
							{
								//if(  nodelink->node_web->loop_web >0) //第二圈的新文章需要下载，但降级0
								if(nodelink->loop_link_father > 1 || 1 == nodelink->threadinfo->nodeWQ->always_download)
								{
										 ifdownload  = 1;
										// nodelink->layer=0;// 会引起// LoopBig.wget_depth计算错误; 降为末级链接，下载之后，不再做分析*************************************************
								}
								else
									ifdownload =0;
							}
						}
						else //老链接
						{

							if(link_is_info_or_channel(conn,nodelink->linknew) != IsInfo)
								ifdownload  = 1;
							else //是信息
								ifdownload =0;
						}


				}

				if(1 ==  ifdownload)
				{
					//这个节点移动出这个队列

					return nodelink;//DeleteQLfront(QLWgetWaiting);

				}
				else
				{
					//DeleteQLWget_QLWgetWaiting(conn,  QLWgetWaiting ,ThreadInfo,1) ;
					nodelink->download_link  = nodelink->download_database;  //不改变
					unlock_link_md5(conn,  nodelink);
					//freeQNodeLink(nodelink);
					return NULL;
				}
		}
		else
		{
			//freeQNodeLink(nodelink);
			//DeleteQLWget_QLWgetWaiting(conn,  QLWgetWaiting ,ThreadInfo ,0) ;
			return NULL;
		}
		return NULL;

}
char *get_str_end(char *str, char c)
{
	char *p=str+1;
	while(*p != '\0')
	{
		if(*p == c) return p;
		p++;
	}
	return p;

}
int clear_link(char *link)
{
	//一些链接带有session等无用的参数，需要去掉，否则会产生大量这个网站的转载信息
	//http://m.sohu.com/n/556530674/?wscrid=1150_1&_smuid=0riLr6U8PBX74ksJT7aNQR&v=2
	char *p;
	if( 1 == checkWeb(link,"m.sohu.com")  ){
		p = index(link,'?');
		if(p)  *p = '\0';
	}
	//http://hf.house.sina.com.cn/news/2015-12-24/16406085710409615330856.shtml?wt_source=newshp_news_23
	else if(1 == checkWeb(link,"hf.house.sina.com.cn"))
	{
		p = strstr(link,"?wt_source=");
		if(p)  *p = '\0';
	}
	else if(1 == checkWeb(link,"guba.sina.com.cn/?s=thread"))
	{
		/*
		http://guba.sina.com.cn/?s=thread&bid=2229&tid=44861
		http://guba.sina.com.cn/?s=thread&tid=44861&bid=2229
		http://guba.sina.com.cn/?s=thread&tid=44861&bid=2229&page=1
		*/
		char  *tid=  strstr(link,"&tid="),*bid=  strstr(link,"&bid=");
		if(tid && bid)
		{
			//置换标准位置 http://guba.sina.com.cn/?s=thread&tid=44861&bid=2229
			//标准
			if(tid > bid)
			{
				int len;
				char *tid_end = get_str_end(tid,'&') ,tid_buf[100];
				len = tid_end - tid;
				strncpy(tid_buf,tid, len);
				tid_buf[len]='\0';

				char *bid_end = get_str_end(bid,'&') ,bid_buf[100];
				len = bid_end - bid;
				strncpy(bid_buf,bid, len);
				bid_buf[len]='\0';

				len = strlen("http://guba.sina.com.cn/?s=thread");
				link[len] = '\0';
				strcat(link,tid_buf);
				strcat(link,bid_buf);
				//printf("[%s]----------------------\n" , link);
			}
		}

	}
	//20180317
	else if( 1 == checkWeb(link,"dealer.autohome.com.cn") && strstr(link , "/news_" ) ){
			//https://dealer.autohome.com.cn/2054063/news_194063138.html?siteID=49
			//https://dealer.autohome.com.cn/2054063/news_194063138.html?siteID=49&pvareaid=2015141
			p = strstr(link,"?");
			if(p)  *p = '\0';
	}
	else if( 1 == checkWeb(link,"dealer.xcar.com.cn")  && strstr(link , "/market_" ) ){
			//http://dealer.xcar.com.cn/115209/market_50805642.htm?zoneclick=100935
			//http://dealer.xcar.com.cn/115209/market_50805642.htm
			p = strstr(link,"?");
			if(p)  *p = '\0';
	}
	else if( 1 == checkWeb(link,"dealer.bitauto.com")  && strstr(link , "/news/" ) ){
			//http://dealer.bitauto.com/100019688/news/201803/169169788.html?leads_source=p032007
			//http://dealer.bitauto.com/100019688/news/201803/169169788.html
			p = strstr(link,"?");
			if(p)  *p = '\0';
	}
	//20180912
	else if( 1 == checkWeb(link,"bbs.tianya.cn")  ){
			//http://bbs.tianya.cn/list.jsp?item=develop&nextid=1536691924000
			p = strstr(link,"&nextid=");
			if(p)  *p = '\0';
	}



	//一般来说，url当中的#号是一个锚点的标志位，这样的url打开之后会将访问者的视线定位在指定位置上，令访问者直接看到网页中间的一段内容。
	//http://www.chinaz.com/web/2014/1105/372993.shtml
	p = index(link,'#');
	if(p)  *p = '\0';

	//http://www.bibet.com/forum.php?mod=redirect&tid=80136&goto=lastpost
	p = strstr( link,"&goto=lastpost");
	if(p)  *p = '\0';

	//https://www.toutiao.com/a6588299760677945869//
	int len = strlen(link);
	if( len > 2 && '/'==link[len-2] &&  '/'==link[len-1] )
		link[len-1] = '\0';

	//20180918
	//http://news.agropages.com/news/ggtj.aspx?id=213&ReUrl=http://www.eastman.com/Markets/agricultural/AgChem-Intermediates/Pages/Overview.aspx?utm_source=AGC-6034&utm_medium=Online-ad&utm_campaign=Agropages-Chinese-homepage-AGC-6034-2018_EastmanAgChem-homepage
	p = strstr( link,"=http");
	if(p) {
		p++;
		sprintf(link ,"%s",p);
	}
	//http%3A%2F%2Ftag.120ask.com%2Fjibing%2Fyfxgxy%2Flist%2F%3Fp%3D68&from=en&to=zh-CHS&tfr=web&domainType=sogou
	//http://www.w3school.com.cn/tags/html_ref_urlencode.html
	if(index(link , '%')){
		ReplaceStr(link,"%3A",":");
		ReplaceStr(link,"%2F","/");
		ReplaceStr(link,"%3F","?");
		ReplaceStr(link,"%3D","=");
	}
	ReplaceStr(link,"&amp;","&");
	return 0;
}
int get_str_begin_end(char *str,char *tag_begin,char *tag_end,char *newstr)
{
	//提取2个关键词之间的内容
	char *p,*pp;
	p = strstr( str , tag_begin);
	if(p)
	{
		p = p +strlen(tag_begin);
		pp = strstr( p , tag_end);
		if(pp)
		{
			if(pp-p <  500  )
			{
				char tmp[1000];
				strncpy(tmp,p,pp-p);
				tmp[pp-p] =  '\0';

				if(NULL == strstr(tmp,"</"))  //不能有其他标签 http://www.cqqjnews.cn/qijiang_Department/Department31/2015-10/08/content_3963361.htm
				{
					//strncpy(newstr,p,pp-p);
					//newstr[pp-p] =  '\0';
					sprintf(newstr,"%s" , tmp);
					//clear_str(newstr);
					//clear_title_some(newstr);
					return 1;
				}
			}
		}
	}
	return 0;

}
int check_str_isdigit(char *str)
{
	//清理字符串中的数组，主要是论坛中有类似情况
	char *p;
	p =str;
	while(*p != '\0')
	{
		if(isdigit(*p))
		{

		}
		else
		{
			return 0;
		}
		p++;
	}
 	return 1;
}
#define weixinlen 120
int do_digui_my_parse (MYSQL *conn,  struct QNodeLink *node_now,struct THREADINFO *ThreadInfo , char *sourcehtml)// , struct ADDWGETNUM*addwgetnum )
{

		struct LINKTITLE linktitle ;
		//char webmd5[MD5_DIGEST_LENGTH*2+1];
		char *begin,*p_end,*p_head,*p,tmp[200];
		int parse_link_return,tm,i,frame=1,window_location_href=1 ,refresh=1;
		int   norepeat=0 ,ifdownload;//,weixinlen =120;


		struct QListMd5 *QLMd5 =(struct QListMd5*)malloc(sizeof(struct QListMd5));
		InitQLMd5(QLMd5);
		InsertQLMd5(QLMd5, node_now->md5);
		//char md5_buf[md5_buf_size];
		//sprintf( md5_buf,"%s" , node_now->md5);

		//node_now->parselinknum =0;


		//合成目标目录
		tm=time((time_t *) NULL);

	      //对parse文件每一行进行链接和标题的提取
		tm=time((time_t *) NULL);
		New_Tolower_Str(sourcehtml); //把<>内的字母变换成小写的,不破坏正文的大小写


		parse_link_return=0;
		begin = sourcehtml;

		p_head = strstr(sourcehtml,"</head>");

		int sourcehtml_len =  strlen(sourcehtml);
		if(p_head == NULL)
		{
			p_end = begin + sourcehtml_len ;
			if(begin + 1024 < p_end)
				p_head = begin +1024;
			else p_head = p_end;

		}
		if(sourcehtml_len > 1024)
		{
			refresh = 0;
			frame= 0 ;
			window_location_href = 0;
		}
		else
		{
			//小文件强制寻找
			//http://epaper.anhuinews.com/
			p_head = begin + sourcehtml_len ;

		}
		//删除注释信息20171215
		Del_str_bengin_to_end_add_a_space(sourcehtml , "<!--","-->");

		int ifcheck_sohu = 0;
		int len;
		i = 0;
		while(  1 )
		{
				//针对页面中提取的每个链接进行递归下载
				linktitle.title[0]='\0';
				linktitle.link[0]='\0';
				linktitle.md5[0]='\0';
				i++;
				if(i==1 && refresh>0)
				{
					if(get_refresh( conn,node_now, sourcehtml ,&linktitle , p_head) < 1) continue;
					linktitle.layer =   node_now->layer;
				}
				else if( frame >0)
				{
					 frame  = 0;
					 if( get_refresh( conn,node_now  , sourcehtml ,&linktitle , p_head) < 1) continue;
					 linktitle.layer =   node_now->layer;
				}
				else if(window_location_href > 0 && node_now->web_or_link == IsWeb)
				{
					window_location_href  = 0; //只取一次
					if( get_window_location_href( conn,node_now , sourcehtml ,&linktitle , p_head) < 1) continue;
					linktitle.layer =  node_now->layer;
				}
				else
				{
					linktitle.layer = node_now->layer -1;
					begin  = parse_link(conn,node_now->threadinfo->myid,node_now->linknew, begin,   &linktitle ,&parse_link_return ,node_now )  ;
					if(parse_link_return < 1)
					{
						//针对http://mt.sohu.com/other/无法解析下一页的问题，在页面中追加一组链接  20160811
						if(0 == ifcheck_sohu && 1 == checkWeb(node_now->linknew,"mt.sohu.com") ){
							ifcheck_sohu = 1;
							char maxPagestr[500],maxPage[500],*p,*pp,linkmain[500];
							if(1 ==  get_str_begin_end(sourcehtml,"var maxPage = " , ";" , maxPage) && 1 == check_str_isdigit(maxPage)){

									p = rindex(node_now->linknew,'/');
									if(p)
									{
										pp = node_now->linknew;
										strncpy(linkmain,pp ,p-pp);
										linkmain[p-pp] = '\0';
										int n,maxPageDigit;

										sourcehtml[0] = '\0';//********************************88

										for(n=0;n<50;n++)
										{
											//http://mt.sohu.com/other/index_1678.shtml
											maxPageDigit = atoi(maxPage) + n;
											sprintf(maxPagestr,"<a href=\"%s/index_%d.shtml\" target=\"_blank\">aaaaaaa</a>  ",linkmain,maxPageDigit);
											//printf("[%s]\n" , maxPagestr);
					    						strcat(sourcehtml,maxPagestr);
										}
										begin = sourcehtml;
										continue;
									}
							}
						}


						break;
					}
					//if(checkLinkFirst(linktitle.link  , strlen(linktitle.link )) <1 )    continue;
				}
				//len = strlen(linktitle.link );
				//if(checkLinkFirst(linktitle.link  , len) <1 )    continue;
				 //printf("%d[%s]\n" , i, linktitle.link);
				//printf("%d[%s]\n" , i, linktitle.title);
				//len = strlen(linktitle.link);
				 /*
				if(strstr(linktitle.link, "//mp.weixin.qq.com") ){
					printf("%d[%s]\n" , i, linktitle.link);
					printf("%d[%s]\n" , i, linktitle.title);
				}
				 */
				clear_link(linktitle.link);
				//printf("%d[%s]\n" , i, linktitle.link);

				if(  IsWeb == node_now->node_web->nodeWQ->type ) {
					//链接基础检查
					if(0 == checkLinkFirst(linktitle.link , strlen(linktitle.link)) )
						continue;
					//域内检查
					if(NO  == node_now->node_web->ifout ){
						if(	NO == checkDomain(node_now ,linktitle.layer, linktitle.link ) )
							continue;
					}
					//出域检查
					else{
						//出域链接检查，这里还必须检查那些链接是否屏蔽了，比如http://www.sina.com.cn/sell  大概500个，还会不断增长，必须想个好办法解决
						if( NO == CheckDomainOut(conn , node_now , linktitle.link , linktitle.layer ))
							continue;
					}
				}
				//检查搜索引擎链接，包括微信  now_linkinfo->threadinfo->nodeWQ->type == IsSearch &&
				else {
					if( NO == CheckLinkSearch(conn , node_now , linktitle.link , linktitle.layer ) )
						continue;
				}

				if(MyDebug > 0) printf("[%s]\n",linktitle.link);

				//clear_link(linktitle.link);
				/*
				if(strstr(linktitle.link, "//mp.weixin.qq.com") ){
					printf("BBBBB%d[%s]\n" , i, linktitle.link);
					printf("BBBBB%d[%s]\n" , i, linktitle.title);
				}
				*/
				//-----------------------------------
				//生成md5
				//-----------------------------------
				if(2<1 &&  1 == checkWeb(linktitle.link,"mp.weixin.qq.com/s") ) {
					//微信截取120字符未md5
					//http://mp.weixin.qq.com/s?src=3&timestamp=1479367849&ver=1&signature=mplzdCM2GJCcZ8Ws2hRurFLK57wz1b6adFiaiFuicpurwnbYz27xl5TzFUCzyiN8cXvNeIlt1acfptcLH7oDqaRNkyfxii1upPU6VaDPGwu4WSL6ipFRsipPRLZeo0TU9WCM59MP27lKNjvA0k2x6iiw1YUvYatsHlhwuy9ndgk=

					//src=3&timestamp=1479348451&ver=1&signature=jygQUzZQgDWPnpmCo3Qp3uWxOHU8Wo8sOjRBWBssA*CWmwq-ZpO4GwwqD3RYNmr0-r*SCSfjiR9RrMfDQ9q5m5jPcJ0DYUnR8FS3SW2WoIfsDciKQlpvzh2Y7x9WJlIWX2p764Bj2emPvgDsuCf23BYUPl3RJZTSH*xciT2hziw=
					//src=3&timestamp=1479353190&ver=1&signature=jygQUzZQgDWPnpmCo3Qp3uWxOHU8Wo8sOjRBWBssA*CWmwq-ZpO4GwwqD3RYNmr0-r*SCSfjiR9RrMfDQ9q5m5jPcJ0DYUnR8FS3SW2WoIfsDciKQlpvzh2Y7x9WJlIWTP0w7n55W292BL1BiWQzMxCb0HNhxcZ-S20gxHQR1Ts=
					//printf("[%s]\n",linktitle.link);
					p = strstr(linktitle.link,"signature=");
					if(p && strlen(p) > weixinlen){
						strncpy(tmp,p,weixinlen);
						tmp[weixinlen]='\0';
						md5_gen_link(linktitle.md5, tmp);
					}
					else
						md5_gen_link(linktitle.md5, linktitle.link);
				}
				else if(checkWeb(linktitle.link,"mp.weixin.qq.com/s") ) {
					//微信连接是时间戳，所以去重改位标题。
					if('\0' == linktitle.title[0])
						continue;
					md5_gen_link(linktitle.md5, linktitle.title);
				}
				else if( 1 == checkWeb(linktitle.link,"da.3g.cn/s.php?idf=")){
					//http://da.3g.cn/s.php?idf=49.1779.11585.115857&sid=&waped=9&gaid=&rd=14807323826462&wid=&pvs=
					//http://da.3g.cn/s.php?idf=49.1779.11585.115857&sid=&waped=9&gaid=&rd=14807295480493&wid=&pvs=
					p = strstr(linktitle.link,"&sid=");
					if(p  ){
						*p='\0';
					}
					md5_gen_link(linktitle.md5, linktitle.link);
				}
				else
					md5_gen_link(linktitle.md5, linktitle.link);

				//-----------------------------------
				//搜索本页中是否md5重复
				//-----------------------------------
				if(1 == find_in_QLMd5(QLMd5,linktitle.md5))
					continue;
				else
					InsertQLMd5(QLMd5, linktitle.md5);


				//printf("%d[%s]\n" , i, linktitle.link);
				//printf("%d[%s]\n" , i, linktitle.title);

				//printf("do_digui_my_parse[%s]\n", linktitle.link );
				norepeat++;

				node_now->parselinknum++;

				//----------------------------------------------------------------------------------
				QNodeLink* nodeson = create_new_node_link( ThreadInfo,node_now->node_web,linktitle.layer,IsLink,Download_OKInit ,strlen(linktitle.link) ,strlen( linktitle.title) ,node_now->loop_link);

				sprintf(nodeson->linknew,"%s" ,linktitle.link);
				if(linktitle.title[0] != '\0')  sprintf(nodeson->titlenew ,"%s",   linktitle.title );

				sprintf(nodeson->md5 , "%s" ,linktitle.md5);

				sprintf(nodeson->SNUID,"%s" , node_now->SNUID);
				sprintf(nodeson->md5_father,"%s" , node_now->md5);
				//--------------------------------------------------------------------------------

			 	if(MyDebug>0)
		 		{
		 			char buf[2000];
					sprintf(buf , "my_parse\n[%s]\n[%s]\n\n",linktitle.link ,linktitle.title);
					Recordwork(buf,Recordparselinkfile);
		 		}
				//printf(  "my_parse\n[%s]\n[%s]\n[%d]\n",linktitle.link ,linktitle.title,linktitle.layer);
				//printf(  "[%s][%d]\n",linktitle.link ,  linktitle.layer);

				ThreadInfo->LoopThreadSmall.link_parse++;

				//InsertQLWaiting(ThreadInfo->QLWgetWaiting,nodeson);
				//nodeson = check_a_nodeLink( conn, nodeson);
				InsertQLWaiting_new( nodeson);


		 }
		//sleep(1000);


		DeleteQLMd5(QLMd5);
		return node_now->parselinknum;

}



const char *
get_string_type(const char *s)
{
#define MAX_MAGIC 16

	  static struct type_map
	  {
	     char magic[MAX_MAGIC];
	     short n_magic;
	     const char *type;
	  } map[] =
	    {
		{{0x42, 0x4d}, 				2, 		"bmp"},
		{{0x47, 0x49, 0x46, 0x38}, 		4, 		"gif"},
		{{0xff, 0xd8, 0xff, 0xe0}, 		4, 		"jpg"},
		{{0x89, 0x50, 0x4e, 0x47}, 		4, 		"png"},
		{{0x42, 0x5a}, 				2, 		"bz"},
		{{0x1f, 0x9d}, 				2, 		"z"},
		{{0x1f, 0x8b}, 				2, 		"gz"},
		{{0x50, 0x4b, 0x03, 0x04}, 		4, 		"zip"},
		{{0x4d, 0x5a}, 				2, 		"exe"}, //windows,ms-dos或os/2 可执行文件
		{{0x7f, 0x45, 0x4c, 0x46}, 		4, 		"elf"}, //unix可执行文件
		/**
		  *	bcmp函数第三个参数为0时，返回0.
		  *	这样就可以在前边的条目失配的情况下匹配此项，
		  *	从而返回该返回的unknown.
		  */
		{{'\0'}, 						0, 		"unknown"}
	    };

	  char buf[MAX_MAGIC];
	  int nread;
	  int i;

	  memset(buf, '\0', sizeof(buf));

	  nread = strlen(s);
	  nread = nread < MAX_MAGIC ? nread : MAX_MAGIC;
	  memcpy(buf, s, nread);

	  for(i = 0; i < sizeof(map) / sizeof(map[0]); ++i)
	       if(0 == bcmp(map[i].magic, buf, map[i].n_magic))
	    break;

	  return map[i].type;
#undef MAX_MAGIC
}




int getlinkmd5bydeletedigit(char *webmd5, char *link)
{

	//把链接中的数字去掉，生成MD5码
	char   *p,*pp,linkbak[1000];

	//http://culture.ifeng.com/whrd/detail_2012_09/07/17430853_0.shtml
	sprintf(linkbak , "%s",link);
	p =  linkbak;
	p = p+ 7;
	if(p)
	{
		pp = index(p,'/');
		if(pp)
		{

			pp++;
			//p = pp;
			while(*pp != '\0')
			{
				if(isdigit(*pp)) *pp = ' ';
				pp++;
			}
			Del_other( linkbak);
			//printf("[%s]\n[%s]\n",link,linkbak);

			md5_gen_link(webmd5, linkbak);
			return 1;
		}
		else return 0;

	}
	else return 0;



}
int parse_weibo( MYSQL *conn ,QNodeLink* node2,struct THREADINFO *ThreadInfo,char *sourcehtml ,char *str_begin,char *str_end,char *str_time,char *pagetitle ){
	//新浪微博 "<!-- feed -->","<!-- /feed -->","class=\"feed_from W_textb" ,"sina_weibo"
	//"<!--card-wrap-->","<!--/card-wrap-->","class=\"from","sina_weibo"
	//<!--微博内容-->,<!--/微博内容-->,"class=\"from","sina_weibo"
			char *begin , *end ,*getlinkbegin  , *getlinkend  ,*p;
			//struct LINKINFO   weibo_linkinfo ;
			int newlinknum,len,Maxlen=500;
			if(MyDebug>0) printf("%s\n" , node2->linknew);
			QNodeLink* node_weibo = create_new_node_link( ThreadInfo,node2->node_web,node2->layer-1,IsLink,Download_OKInit ,Maxlen,Maxlen,node2->loop_link);
			/*
			QNodeLink* node_weibo;
			node_weibo=(QNodeLink*)malloc(sizeof(QNodeLink));
			node_weibo->linknew= (char *)malloc(500);
			node_weibo->titlenew= (char *)malloc(500);

			nodelink_inherit(node2,node_weibo,node2->layer-1);
			*/
			//解析sina微博的搜索结果，依据网页中的标签，有可能修改
			//begin  = strstr(sourcehtml,"<div class=\"WB_cardwrap S_bg2 clearfix\"");
			char *newp;
			newp = sourcehtml;

			int n = 0,num=0;
			while(1)
			{
				begin  = strstr(newp,str_begin);
				if(begin == NULL ) break;
				//end = strstr(begin+50 , "<div class=\"WB_cardwrap S_bg2 clearfix\"");

				end = strstr(begin+50 , str_end);

				if(end == NULL ) break;

				*end = '\0';
				//把链接提取出来
				getlinkbegin = strstr(begin ,str_time);
				if(getlinkbegin == NULL ) break;
				getlinkbegin = strstr(getlinkbegin ," href=\"http");
				if(getlinkbegin == NULL ) break;

				getlinkbegin = strstr(getlinkbegin ,"http");
				getlinkend = strstr(getlinkbegin ,"\"");
				if(getlinkend == NULL ) break;
				len = getlinkend-getlinkbegin;
				//printf("parse_weibo  len =%d \n"  , len );
				//20170128
				if(len > Maxlen) {
					*end = '<';
					newp = getlinkend;
					continue;
				}
				strncpy(node_weibo->linknew,getlinkbegin, len);
				node_weibo->linknew[len]='\0';
				p = strstr(node_weibo->linknew,"?type");
				if(p) *p = '\0';

				//20180925 去掉新浪微博链接尾部无用信息
				//https://weibo.com/3806727407/GAGHDbjBh?refer_flag=1001030103_
				if(strstr(node_weibo->linknew,"/weibo.com/") ){
					p = index(node_weibo->linknew,'?');
					if(p) *p = '\0';
				}

				sprintf(node_weibo->titlenew, "%s" ,pagetitle);

				Del_other(node_weibo->linknew);
				convert_unicode(node_weibo->linknew);
				if(checkLinkFirst(node_weibo->linknew, strlen(node_weibo->linknew)) >0  )    // &&   checkLinkSecond(conn,QLShieldWeb ,node_weibo->linknew) >0
				{
					if(MyDebug>0) printf("[%s]\n" , node_weibo->linknew);
					//weibo_linkinfo.linkhash  = Str2int_map(weibo_linkinfo.link);
					md5_gen_link(node_weibo->md5, node_weibo->linknew);

					//printf("  weibo ----------------------------------------\n");
					node_weibo->query_return  = lock_link_md5( conn, ThreadInfo, node_weibo);
					if(LinkError == node_weibo->query_return)
						break;
					else if(LinkNew == node_weibo->query_return )
					{

						do_new_file(   node_weibo, ThreadInfo ,  begin);
						unlock_link_md5(conn,    node_weibo );
					}
					else if(Link_Locked == node_weibo->query_return )
					{
						unlock_link_md5(conn,   node_weibo );
						//break;
					}
					//printf("%d\n" , n);
					n++;
				}
				*end = '<';
				newp = end+1;
				//node2->num_caiji++;
				node2->parselinknum++;
			}
			//printf("  %s---%d/%d----[%s]-\n",pagetitle,n,node2->num_caiji,ThreadInfo->wget_html);

			if(n<1 ) newlinknum = 0;
			else newlinknum = Download_OKForever;

			freeQNodeLink(node_weibo);
			//free(node_weibo->linknew);
			//free(node_weibo->titlenew);
			//free(node_weibo);
			return newlinknum;

}

#define BUF_SIZE    4096*2
int file_copy(const char *src, const char *dest, mode_t mod)
{
	FILE *in_file, *out_file;
	char data[BUF_SIZE];
	size_t bytes_in, bytes_out;
	long len = 0;

	if ( (in_file = fopen(src, "rb")) == NULL )
	{
		perror(src);
		return 2;
	}
	if ( (out_file = fopen(dest, "wb")) == NULL )
	{
		perror(dest);
		return 3;
	}


	while ( (bytes_in = fread(data, 1, BUF_SIZE, in_file)) > 0 )
	{
		bytes_out = fwrite(data, 1, bytes_in, out_file);
		if ( bytes_in != bytes_out )
		{
			perror("Fatal write error.\n");
			return 4;
		}
		len += bytes_out;
		//printf("copying file .... %d bytes copy\n", len);
	}

	fclose(in_file);
	fclose(out_file);
	return 1;
}
int  parse_weibo_qq( MYSQL *conn ,QNodeLink* node_link_now,struct THREADINFO *ThreadInfo,char *sourcehtml )
{

		/*
			<li id="29345107753802" tm="1334822909">
				<!-- 正文作者头像 -->
				<div class="userPic">
							<a target="_blank" title="马磊" href="http://t.qq.com/BCBG969317636" rel="马磊">
						<!-- todo -->
									<!--todo<img onerror="MI.Pic（this，50)" src="http://t0.qlogo.cn/mbloghead/fa0cf04bb5a94c137bc0/50" />-->
						<img width="50" height="50" src="http://t0.qlogo.cn/mbloghead/fa0cf04bb5a94c137bc0/50" onerror="this.src='img/normal_avatar.jpg'">
								</a>
						</div>

				<!-- 正文 -->
				<div class="msgBox">

					<!-- 用户昵称 -->
					<div rel="BCBG969317636" class="userName">
						<stong><a title="马磊" href="http://t.qq.com/BCBG969317636" target="_blank">马磊</a></stong>:
					</div>

					<!-- 正文文本 -->
					<div class="msgCnt">经营：茅台 五粮液（1618） 水井坊 <em>剑南春</em> 国窖(1573) 汾酒（三十年 老白汾53度 45度） 青花瓷(二十年） 红花郎 洋</div>

					<!-- 正文图片-->


					<!-- 转载源文内容和图片-->
							<div class="k"></div>

					<!-- 正文发表时间、操作等操作 -->
					<div class="pubInfo">
						<cite>腾讯微博</cite>&nbsp;-&nbsp;
						<span class="gr timespan" t="270" st="1334823179">18分钟前</span>
					</div>
				</div>
			</li>

			*/
			int len, newlinknum;
			int n = 0,num=0;
			char *begin , *end ,*getlinkbegin  , *getlinkend  ,*p;
			if(MyDebug>0) printf("%s\n" , node_link_now->linknew);
			char qqweibotmp[100];

			QNodeLink* node_weibo = create_new_node_link( ThreadInfo,node_link_now->node_web,node_link_now->layer-1,IsLink,Download_OKInit ,500,500,node_link_now->loop_link);


			/*
			 QNodeLink* node_weibo;
			 node_weibo=(QNodeLink*)malloc(sizeof(QNodeLink));

			node_weibo->linknew= (char *)malloc(500);
			node_weibo->titlenew= (char *)malloc(500);

			nodelink_inherit(  node_link_now,   node_weibo ,node_link_now->layer-1);
			*/
			begin  = strstr(sourcehtml,"<li id='");
			while(1)
			{
				if(begin == NULL ) break;
				end = strstr(begin+50 , "<li id='");
				if(end == NULL ) break;

				*end = '\0';
				//把链接提取出来
				getlinkbegin = begin + 8;
				getlinkend = strstr(getlinkbegin ,"'");
				if(getlinkend == NULL ) break;
				len = getlinkend-getlinkbegin;
				if(len>50) break;
				strncpy(qqweibotmp ,getlinkbegin, len);
				qqweibotmp[len]='\0';
				sprintf(node_weibo->linknew, "http://t.qq.com/p/t/%s" , qqweibotmp);

				sprintf(node_weibo->titlenew , "qq_weibo");

				Del_other(node_weibo->linknew);
				convert_unicode(node_weibo->linknew);
				if(checkLinkFirst(node_weibo->linknew, strlen(node_weibo->linknew)) >0  )    //&&   checkLinkSecond(conn,QLShieldWeb ,node_weibo->linknew) >0
				{
					if(MyDebug>0) printf("[%s]\n" , node_weibo->linknew);

					//weibo_linkinfo.linkhash  = Str2int_map(weibo_linkinfo.link);
					md5_gen_link(node_weibo->md5, node_weibo->linknew);

					//weibo_linkinfo.webid = 0;
					node_weibo->query_return  = lock_link_md5( conn, ThreadInfo,node_weibo);
					if(LinkError == node_weibo->query_return)
						break;
					else if(LinkNew == node_weibo->query_return )
					{
						do_new_file(  node_weibo, ThreadInfo ,  begin);
						unlock_link_md5(conn,   node_weibo );
					}
					else if(Link_Locked == node_weibo->query_return )
					{
						unlock_link_md5(conn,   node_weibo );
						//break;
					}
					//printf("%d\n" , n);
					node_link_now->parselinknum++;
					n++;
				}
				*end = '<';
				begin = end;
			}
			if(n<1 ) newlinknum = 0;
			else newlinknum = Download_OKForever;
			if(0 == newlinknum ||  newlinknum ==  Download_OKForever)  newlinknum =1; //有可能解析出0，但文件是好的，所以+1


			freeQNodeLink(node_weibo);
			//free(node_weibo->linknew);
			//free(node_weibo->titlenew);
			//free(node_weibo);


}
int get_cookie_filename(char * md5,char *WgetWorkDir ,char *cookie_file )
{

	sprintf(cookie_file,"%swgetcookie_%s.txt", WgetWorkDir,md5);
}
int get_out_filename(char * md5,char *WgetWorkDir ,char *out_file )
{

	//sprintf(out_file,"  -o %s_outinfo_%s ", WgetWorkDir , md5);
	sprintf(out_file,"%s_outinfo_%s", WgetWorkDir , md5);
}
int get_center_filename(char * md5,char *WgetWorkDir ,char *out_file )
{
	sprintf(out_file,"%s_center_%s", WgetWorkDir , md5);
}
int read_cookie(QNodeLink* node_link_now,struct THREADINFO *ThreadInfo  )
{
	char cookie_file[200];
	get_cookie_filename(node_link_now->md5,ThreadInfo->WgetWorkDir , cookie_file );
	char *sourcehtml = file2strzran(cookie_file) ,*p,*p_end;
	int len,myreturn =0;

	if(sourcehtml == NULL)	{ return -1; }

/*

# HTTP cookie file.
# Generated by Wget on 2015-09-09 20:33:07.
# Edit at your own risk.

.weixin.sogou.com       TRUE    /       FALSE   2072521986      SUID    4FE508AB6B20900A0000000055F02702
weixin.sogou.com        FALSE   /       FALSE   1444393986      ABTEST  7|1441801986|v1
.sogou.com      TRUE    /       FALSE   1473337986      IPLOC   CN4100
.sogou.com      TRUE    /       FALSE   1442665986      SNUID   45EF01A2090C1645A6369D750A38C190
*/
	char tmp[100];
	//printf("read_cookie[%s]\n" , sourcehtml);
	p = strstr( sourcehtml,"SNUID");
	if(p)
	{
		p = p+strlen("SNUID");
		p_end =   strstr( p,"\n");
		if(p_end)
		{
			len = p_end-p;
			strncpy(tmp,p ,len);
			tmp[len] = '\0';
			Del_other(tmp);
			sprintf(node_link_now->SNUID,"%s",tmp);
			myreturn = 1;
		}
		else
			myreturn = -2;
	}
	else
		myreturn = -3;
	free(sourcehtml);

	return myreturn;
}
int read_outfile(QNodeLink* node_link_now,struct THREADINFO *ThreadInfo  )
{
	char out_file[200];
	get_out_filename(node_link_now->md5,ThreadInfo->WgetWorkDir , out_file );
	char *sourcehtml = file2strzran(out_file) ,*p,*p_end;
	int len,myreturn =0;

	if(sourcehtml == NULL)
	{
		printf("NULL-------------[%s]\n" ,out_file);
		//sleep(10000);
		return -1;
	}

/*
--2015-09-10 05:13:56--  http://weixin.sogou.com/websearch/art.jsp?sg=CBf80b2xkgZuOpLU3LU5SWjNncd4Dygq5SuYcKCYz3E9RP9D8aS
NMHsCKAwJkAzOf4qifgwTjBAhoou9bCXtGX7KRMDG_3aVIFCDmAtlzeo.&url=p0OVDH8R4SHyUySb8E88hkJm8GF_McJfBfynRTbN8whMUAHSRE806n4I0xA
onY_QXY6RLCSg2kQ1DyHy2v9YtFMj362uDS1pH-Uzfm8hyzLEQVV22fcfNmq88YLhs2Cm2YGTGO-w1XFYy-5x5In7jJFmExjqCxhpkyjFvwP6PuGcQ64lGQ2Z
DMuqxplQrsbk&SNUID=360C8E6CBEBBA2EB3087FF3CBEE19DF0
正在解析主机 weixin.sogou.com... 61.135.189.35, 123.125.125.114, 61.135.189.36, ...
正在连接 weixin.sogou.com|61.135.189.35|:80... 已连接。
已发出 HTTP 请求，正在等待回应... 302 Found
位置：http://mp.weixin.qq.com/s?__biz=MjM5MzgxNjYxMQ==&mid=209552310&idx=3&sn=f0bc6c9ba066c967febf62c90313b049&3rd=MzA3MD
U4NTYzMw==&scene=6#rd [跟随至新的 URL]
--2015-09-10 05:13:56--  http://mp.weixin.qq.com/s?__biz=MjM5MzgxNjYxMQ==&mid=209552310&idx=3&sn=f0bc6c9ba066c967febf62c9
0313b049&3rd=MzA3MDU4NTYzMw==&scene=6
正在解析主机 mp.weixin.qq.com... 140.206.160.199, 140.207.137.32, 140.207.62.51
正在连接 mp.weixin.qq.com|140.206.160.199|:80... 已连接。
已发出 HTTP 请求，正在等待回应... 200 OK
长度：49212 (48K) [text/html]
正在保存至: “kkk.html”

     0K .......... .......... .......... .......... ........  100%  801K=0.06s

2015-09-10 05:13:56 (801 KB/s) - 已保存 “kkk.html” [49212/49212])
*/
	char tmp[500];
	//printf("[%s]\n" , sourcehtml);
	p = strstr( sourcehtml,"http://mp.weixin.qq.com/");
	if(NULL ==p )
		p = strstr( sourcehtml,"https://mp.weixin.qq.com/");
	if(p)
	{

		p_end =   strstr( p," ");
		if(p_end)
		{
			len = p_end-p;
			strncpy(node_link_now->linknew,p ,len);
			node_link_now->linknew[len] = '\0';
			Del_other(node_link_now->linknew);

			//清除SNUID
			p_end = strstr(node_link_now->linknew,"&SNUID=");
			if(p_end) *p_end = '\0';

			myreturn = 1;
		}
		else
			myreturn = -2;
	}
	else
		myreturn = -3;
	free(sourcehtml);
	//unlink(out_file);
	return myreturn;
}
/*****************************************************************
* 检查链接是否需要重新拨号
******************************************************************/
void restartConnection(){
	char buf[200];
	sprintf(buf,"%s/pppoe.sh " ,NowWorkingDir);
	system(buf);
}
void  checkConnection(struct QNodeWebQueue *nodeWQ ){  //QNodeLink* node_wget
	if(Connection_pppoe_all == nodeWQ->Connection || Connection_pppoe_web == nodeWQ->Connection){
	//if( 1 == PPPOE){
		nodeWQ->NumDownloadError++;
		int maxErrorNum = nodeWQ->num_thread * nodeWQ->NumSHInThread*2  ;//每个sh 允许有2个错误
		if(nodeWQ->NumDownloadError >    maxErrorNum  ){
			printf("type=%d   maxErrorNum =  %d-----------------------------------------------\n" ,nodeWQ->type, maxErrorNum);
			restartConnection();
			//node_wget->node_web->nodeWQ->NumDownloadError =0;
			//初始化所有采集队列的NumDownloadError = 0
			InitQLWebQueue_NumDownloadError(QLWebAll  );
		}
	}
}

int do_wget_downloaded_file(MYSQL *conn ,  QNodeLink* node_link_now  ,struct THREADINFO *ThreadInfo)
{ //处理节点



		//-----------------------------------------------------------------------------------------------------------
		//处理文件---------------------------------------------------------------------------------------------------
		//-----------------------------------------------------------------------------------------------------------

		// 5、读html文件到内存中，并判断下载文件的合理行
		char  filetype[100];
		char *sourcehtml = file2strzran(ThreadInfo->wget_html);
		if(sourcehtml == NULL)	{ return -1; }//这文章处理完了

		//判断解压缩问题
		//New_Tolower_Str(sourcehtml); //把<>内的字母变换成小写的,不破坏正文的大小写

		//http://news.cd.fang.com/2015-04-19/15631144.htm
		//http://blog.163.com/bh_binghu/blog/static/94553512011626102054571/
		sprintf(filetype,"%s" ,get_string_type(sourcehtml) );
		if( strcmp(filetype ,"gz") == 0)
		{
			free(sourcehtml);
			sourcehtml = NULL;
			//printf("a gzip  [%s]\n",ThreadInfo->wget_html);
			//sleep(1000);
			sprintf(ThreadInfo->order_all,"gunzip -c %s >%s",ThreadInfo->wget_html,ThreadInfo->_wget_html);
			system(ThreadInfo->order_all);
			rename(ThreadInfo->_wget_html,ThreadInfo->wget_html);

			sourcehtml = file2strzran(ThreadInfo->wget_html);
			if(sourcehtml == NULL)	 return -7; //这文章处理完了
		}
		else if( strcmp(filetype,"unknown")  != 0) //其他类型的文件一律删除
		{
			//Loop.DownloadError++;
			free(sourcehtml);
			sourcehtml = NULL;
			return -105; //这文章处理完了
		}


		//-----------------------------------------------------------------------
		//二、合成新文件
		//-----------------------------------------------------------------------
		if(2<1 && IsWeiXin == node_link_now->threadinfo->nodeWQ->type  )
		{
			if( IsWeb == node_link_now->web_or_link)
			{
				//读取cookie
				int a = read_cookie(node_link_now , ThreadInfo);
				//printf("SNUID=[%s] %d\n",node_link_now->SNUID,a);
			}
			else
			{
				//读取outfile，获取可以访问的链接，替换linknew
				//int a = read_outfile(node_link_now , ThreadInfo);
				//printf("IsWeiXinlinknew=[%s] %d\n",node_link_now->linknew,a);
			}

		}

		if( 1 == checkWeb(node_link_now->linknew,"s.weibo.com")){    //针对新浪微博搜索采集,提取页面中的链接合成多个新文件
			//20180925 新浪微博切换网页模板，这个阶段的确存在两种格式的网页，估计时新浪部分服务器更新了程序。
			//新模板
			parse_weibo( conn ,node_link_now,ThreadInfo,sourcehtml,"<!--card-wrap-->","<!--/card-wrap-->","class=\"from","sina_weibo"); //20180925
			//老模板
			if(0 == node_link_now->parselinknum){
				printf("parse_weibo sina  2\n");
				parse_weibo( conn ,node_link_now,ThreadInfo,sourcehtml ,"<!-- feed -->","<!-- /feed -->","class=\"feed_from W_textb" ,"sina_weibo");
			}
		}
		else if( 1 == checkWeb(node_link_now->linknew,"t.qq.com")) {//针对QQ微博搜索采集,提取页面中的链接合成多个新文件
			parse_weibo_qq( conn ,node_link_now,ThreadInfo,sourcehtml );
		}
		else if( 1 == checkWeb(node_link_now->linknew,"t.zhongsou.com")) { //godreply_on
			parse_weibo( conn ,node_link_now,ThreadInfo,sourcehtml ,"<div class=\"godreply_on\" ","<div class=\"godreply_on\" ","class=\"weibo_time" ,"zhongsou_weibo");
		}
		else if(strstr(node_link_now->linknew, "tn=baiduwb")){  //godreply_on
			parse_weibo( conn ,node_link_now,ThreadInfo,sourcehtml ,"<li id=\"","<li id=\"","<a class=\"weibo_al\"" ,"baidu_weibo");
		}
		else{   //处理网页信息

				//------------------------------------
				// 1、 是否生成新文件
				//-----------------------------------
				if(node_link_now->web_or_link == IsLink &&  node_link_now->query_return == 2 &&   (node_link_now->loop_link_father > 1 || 1 == node_link_now->threadinfo->nodeWQ->always_download || IsWeiXin == node_link_now->threadinfo->nodeWQ->type ))// node_link_now->threadinfo->nodeWQ->type == IsWeiXin  ))//&& node_link_now->node_web->loop_web > 0 )  //now_linkinfo->query_return == 2是新链接，1是老链接，0是被别的锁定，-1是异常
				{
					//printf("4444444444444444444444444444\n");
					do_new_file(  node_link_now, ThreadInfo ,  sourcehtml);
				}

				//------------------------------------
				// 2、 是否下载儿子链接
				//-----------------------------------
				if(node_link_now->layer > 0  )
				{
					//-----------------------------------------------------------------------
					//三、提取页面中的链接,插入wget任务队列
					//-----------------------------------------------------------------------
					//检查链接模式是正文页面，还是频道页面，正文页面是不采集的
					//char webmd5[MD5_DIGEST_LENGTH*2+1];


					//是文章不分析了,//允许微信文章分析网页提取新链接
					if( node_link_now->web_or_link == IsLink   &&   link_is_info_or_channel(conn,node_link_now->linknew) == IsInfo  ) // NULL == strstr(node_link_now->linknew,"http://mp.weixin.qq.com/")  && IsWeiXin != node_link_now->threadinfo->nodeWQ->type
					{

					}
					else
						do_digui_my_parse(conn,node_link_now, ThreadInfo ,  sourcehtml);// , &addwgetnum );

				}


		}

		//搜索引擎网页检查，微博网页检查，微信检查
		if(IsWeb == node_link_now->web_or_link   &&  IsWeb != node_link_now->node_web->nodeWQ->type  )// )   node_link_now->node_web->nodeWQ->index_proxy > -1
		{
			int proxy_index;
			if(node_link_now->node_proxy)
				proxy_index = node_link_now->node_proxy->index;
			else
				proxy_index = -1;
			printf("%d--------%20s---%2d ----%3dk---proxy_index=  %d \n",node_link_now->threadinfo->myid , node_link_now->node_web->nodeWQ->web, node_link_now->parselinknum, (int)((float)strlen(sourcehtml) /1024.0), proxy_index);
			//if(IsWeibo == node_link_now->node_web->nodeWQ->type  &&  node_link_now->parselinknum <1)
			//	checkConnection(node_link_now);

		}

		free(sourcehtml);
		sourcehtml = NULL;
		return 1;

}




int kill_process(char *killkey )
{
	//remove(_wget_info);

	char buf[500];
	sprintf(buf , "ps -efww|grep %s |grep -v grep|cut -c 9-15|xargs kill " , killkey);
	system(buf);
	return 0;
}
int add_nodeSH(struct QListSH *QLTaskSH , struct QNodeSH *nodeSH)
{
	//给队列加一个节点
	if(NULL == QLTaskSH->end) //空队列
	{
		QLTaskSH->front= nodeSH;
		QLTaskSH->end = nodeSH;
		nodeSH->next = NULL;
		nodeSH->forward= NULL;
	}
	else
	{
		nodeSH->forward = QLTaskSH->end;
		QLTaskSH->end->next = nodeSH;
		QLTaskSH->end = nodeSH;
		nodeSH->next = NULL;
	}
}
struct QNodeSH * move_nodeSH(struct QListSH *QLTaskSH_src, struct QNodeSH *nodeSH,struct QListSH *QLTaskSHWaiting_target)
{
	//printf("111111111  src=%d    target=%d\n" , count_SH(QLTaskSH_src,0)   , count_SH(QLTaskSHWaiting_target,0)  );

	//if(QLTaskSH_src->front == QLTaskSHWaiting_target->front) return NULL;

	//删除原来的节点
	//删除头节点返回NULL
	struct QNodeSH  *nodeSH_next;
	if(NULL == nodeSH->forward) //是头节点
	{
		if(NULL == nodeSH->next)//队列只有一个节点
		{
			QLTaskSH_src->front = NULL;
			QLTaskSH_src->end = NULL;
			nodeSH_next = NULL;
		}
		else //是头，但有多个节点
		{
			QLTaskSH_src->front = nodeSH->next;
			QLTaskSH_src->front->forward = NULL;
			nodeSH_next = QLTaskSH_src->front;
		}
	}
	else
	{
		if(NULL == nodeSH->next ) //尾部节点
		{
			QLTaskSH_src->end = nodeSH->forward;
			QLTaskSH_src->end->next = NULL;
			nodeSH_next = NULL;
		}
		else //中间节点
		{
			nodeSH->forward->next= nodeSH->next;
			nodeSH->next->forward = nodeSH->forward;
			nodeSH_next = nodeSH->next;
		}
	}

	//添加到队列中
	add_nodeSH(QLTaskSHWaiting_target , nodeSH);

	//printf("222222222  src=%d    target=%d\n" , count_SH(QLTaskSH_src,0)   , count_SH(QLTaskSHWaiting_target,0)  );
	//返回原来的队列被移动节点的下一个节点
	return nodeSH_next;
}

int Move_a_node_to_QL(struct QList* QLtarget, QNodeLink* p)
{

	p->next = NULL;
	if(QLtarget->front==NULL)
	{
		    QLtarget->front=p;
		    QLtarget->end=p;

	}
	else
	{
		    QLtarget->end->next=p;
		    QLtarget->end=p;
	}

	return 0;

}
int Move_node(struct QList* QLsource,struct QList* QLtarget ,   struct THREADINFO *ThreadInfo  )
{


	QNodeLink* p;


	if(QLsource->front==NULL)
	{
	    return -1;
	}

	//移出等待队列
	p=QLsource->front;
	if(QLsource->front->next==NULL)
	{
	    QLsource->front = NULL;
	    QLsource->end = NULL;
	}
	else
	{
	    QLsource->front = p->next;
	}



	//插入工作队列
	 p->next=NULL;
	if(QLtarget->front==NULL)
	{
	    QLtarget->front=p;
	    QLtarget->end=p;
	    //p->next=NULL;
	}
	else
	{
			if(IsWeb == p->web_or_link) //插入头部***********************************
			{
				 p->next = QLtarget->front;
				QLtarget->front =p;
			}
			else //插入尾部，通常模式
			{
			    //p->next=NULL;
			    QLtarget->end->next=p;
			    QLtarget->end=p;
			}
	}

	return 0;
}

int Move_node_to_end(struct QList* QL)
{

	QNodeLink* p;

	p = QL->front;
	if(QL->front==NULL || QL->front->next==NULL){printf("only one node \n"); return 0;}
	else
	{
		QL->front = p->next;

		p->next=NULL;
		QL->end->next=p;
		QL->end=p;
	}


	return 1;
}
int update_download_tm(struct QNodeLink *nodelink)
{
		nodelink->begin_wget_download_tm =  time((time_t *) NULL);
	      //if(IsWeb== nodelink->web_or_link )
		//	nodelink->node_web->last_wget_downlaod_tm =  nodelink->begin_wget_download_tm;

		return 0;
}
//*************************************************************************************************************************

struct QNodeProxy *  find_proxy_to_right(  QNodeProxy *node_proxy_begin,int index_proxy )
{
		struct QNodeProxy *node_proxy=node_proxy_begin;
		while(node_proxy  )
		{

			if( node_proxy->good[index_proxy]  < proxy_error)
			{

				return node_proxy;
			}
			node_proxy = node_proxy->next;
		}


	return NULL;
}
int check_node_proxy(QNodeProxy *node_proxy,int index_proxy){
		//pthread_mutex_lock(&mymutex_good_index_proxy);
		//if(proxy_free == node_proxy->good[index_proxy] ) //*********************************************
		if( node_proxy->good[index_proxy] < proxy_error)
		{


			node_proxy->good[index_proxy]++;//=  proxy_busy;
			node_proxy->tm =  time((time_t *) NULL);
			//pthread_mutex_unlock(&mymutex_good_index_proxy);

			return 1;
		}
		//pthread_mutex_unlock(&mymutex_good_index_proxy);

		return 0;
}
struct QNodeProxy *  find_proxy(  QListProxy *QLProxy, QNodeProxy *node_proxy_begin,int index_proxy   )
{
		struct QNodeProxy *node_proxy;

		if( NULL == node_proxy_begin ) { //2>1 ||
			node_proxy = QLProxy->front;

			while(node_proxy  ){
				if(1 == check_node_proxy(node_proxy ,index_proxy))
					return node_proxy;
				node_proxy = node_proxy->next;
			}
		}
		else{
			node_proxy = node_proxy_begin;

			//向右找
			while(node_proxy){
				if(1 == check_node_proxy(node_proxy ,index_proxy))
					return node_proxy;
				node_proxy = node_proxy->next;
			}

			//从开始位置向当前节点找
			node_proxy = QLProxy->front;
			while(node_proxy &&   node_proxy != node_proxy_begin ){
				if(1 == check_node_proxy(node_proxy ,index_proxy))
					return node_proxy;
				node_proxy = node_proxy->next;
			}
		}

		return NULL;

}

int get_proxy_manage(struct QNodeLink* nodelink ,char *proxystr ){
		//只有weninfo的链接使用代理服务器，二级链接不使用
		//int index_proxy = nodelink->threadinfo->nodeWQ->index_proxy;
		//if(index_proxy != NotUseProxy && nodelink->web_or_link == IsWeb && nodelink->threadinfo->node_proxy )
		if(nodelink->node_proxy){
			nodelink->node_proxy = nodelink->threadinfo->node_proxy;
			//sprintf(proxystr , " -e  \"http_proxy=%s\" " ,nodelink->node_proxy->proxy);
			sprintf(proxystr , "%s" , nodelink->node_proxy->proxy);
			//安全地带

			//nodelink->threadinfo->node_proxy =  find_proxy_to_right(  nodelink->node_proxy,  nodelink->threadinfo->nodeWQ->index_proxy );

		}
		else{
			//nodelink->node_proxy = NULL;
			///home/zran/src/wget/src/wget    --timeout=60   --tries=1 --convert-links  -erobots=off  -Q1m    -e  "http_proxy=116.62.128.50:16816" --proxy-user=zran --proxy-passwd=o9wbwatr   --user-agent="Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.3) Gecko/2008092416 Firefox/3.0.3"   -O a.html     --accept=html,htm,shtml,asp,php,jsp     "http://www.163.com"

			proxystr[0] = '\0';
			//sprintf(proxystr , " -e  \"http_proxy=116.62.128.50:16816\"  --proxy-user=zran --proxy-passwd=o9wbwatr " );
		}

		return 0;
}

int get_working_wget_baseinfo( QNodeLink* node2 , char *WgetWorkDir, char *_son_wget_info, char *_wget_html, char *wget_html){


		//sprintf(_son_wget_info,"%u_%d_%u_%u_%d_%d_%s",node2->node_web->webid,node2->layer,node2->loop_link,Str2int_map(node2->linknew),node2->query_return,node2->node_web->nodeWQ->type,node2->md5);
		//sprintf(_son_wget_info,"estarmanzhuawget_%u_%u_%s",node2->index,node2->node_web->webid,node2->md5);
		sprintf(_son_wget_info,"estarmanzhuawget_%d_%s_%s_%d",node2->node_web->webid,node2->md5 , ToolsStr[node2->tools],node2->index);
		sprintf(_wget_html,"%s_%s",WgetWorkDir,_son_wget_info);
		sprintf(wget_html,"%s%s",WgetWorkDir,_son_wget_info);
		return 0;
}
int clear_working_wget_baseinfo(struct THREADINFO *ThreadInfo   ){
		 ThreadInfo->_son_wget_info[0]='\0';
		 ThreadInfo->_wget_html[0]='\0';
		 ThreadInfo->wget_html[0]='\0';
		return 0;
}

char *testfile ="testfile.txt";
char *agent = "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.3) Gecko/2008092416 Firefox/3.0.3";//http://www.icaijing.com/
//char *agent = "User-Agent: Mozilla/5.0 (compatible; MSIE 6.0;Windows XP)";
QNodeSH *  fclose_run_a_sh( struct THREADINFO *ThreadInfo ,QNodeSH *nodeSH)
{
	//写文件SH


	// printf("%2d  index=%d      nodeSH->num_wget=%d  ThreadInfo->num_wget_waiting_all=%d \n" ,ThreadInfo->myid, nodeSH->index,  nodeSH->num_wget ,ThreadInfo->num_wget_waiting_all );
	if( nodeSH->num_wget >0)
	{
		FILE *FILE_SH;
		struct QNodeLink* nodelink;
		char str_onewgetLimitRate[100],  proxystr[100],getproxystr[100],cookie_str[200],cookie_file[200],out_file_str[200];//,center_file[200];
		char order_standard[2000],order_tmp[1000],_son_wget_info[200],_wget_html[200],wget_html[200];
		int ifmove;
		FILE_SH = fopen(nodeSH->shfilename, "w");
		if(FILE_SH == NULL ) {
			printf("creat sh error [%s]\n",nodeSH->shfilename);
			return  nodeSH;
		}
		else{
			sprintf(order_tmp,"#!/bin/sh\n\n");
			fputs( order_tmp,FILE_SH);
		}

		nodelink = nodeSH->QLWget->front;
		while(nodelink){
				//获取代理服务器
			    get_proxy_manage(nodelink , getproxystr);
				//选择下载工具
				//nodelink->tools = DownloadTools_Get(nodelink->linknew , nodelink->node_web->nodeWQ->Tools ,nodelink->web_or_link);
				//合成目标下载的文件名
				//get_working_wget_baseinfo( nodelink,ThreadInfo->WgetWorkDir,_son_wget_info,_wget_html,wget_html);


				//生成标准采集语句
				//--------------------------------------
				nodelink->tools= nodelink->node_web->nodeWQ->Tools ;
				ifmove = 1;
				if(ToolsDirServerAll == nodelink->tools || ToolsDirServerWeb == nodelink->tools  && IsWeb == nodelink->web_or_link ){
					//后台chrome服务器方式
					get_working_wget_baseinfo( nodelink,ThreadInfo->WgetWorkDir,_son_wget_info,_wget_html,wget_html);
					sprintf(order_standard,"echo \"web@@@@@@in@@@@@@%s\">> %s \n " ,nodelink->linknew , _wget_html );
					ifmove = 0;
				}
				else if(ToolsPhantomjsAll == nodelink->tools || ToolsPhantomjsWeb == nodelink->tools  &&  IsWeb == nodelink->web_or_link ){
					get_working_wget_baseinfo( nodelink,ThreadInfo->WgetWorkDir,_son_wget_info,_wget_html,wget_html);
					sprintf(order_standard,"touch %s \n /usr/local/bin/phantomjs spider.js  %s  %s  \n" , _wget_html , nodelink->linknew , _wget_html );
				}
				else if(ToolsChromePythonAll == nodelink->tools || ToolsChromePythonWeb == nodelink->tools  &&  IsWeb == nodelink->web_or_link  ){
					get_working_wget_baseinfo( nodelink,ThreadInfo->WgetWorkDir,_son_wget_info,_wget_html,wget_html);
					sprintf(order_standard,"touch %s \n python3.6 %s/crawlpy/weixin.py  '%s'  '%s'  'weixin'   ''   'headless'  >> chrome.txt\n" ,_wget_html , NowWorkingDir,nodelink->linknew , _wget_html );
				}
				else if(ToolsChromeCommandAll == nodelink->tools || ToolsChromeCommandWeb == nodelink->tools  &&  IsWeb == nodelink->web_or_link  ){
					//无头后台采集方式
					get_working_wget_baseinfo( nodelink,ThreadInfo->WgetWorkDir,_son_wget_info,_wget_html,wget_html);
					sprintf(order_standard,"touch %s \n /opt/google/chrome/chrome  --headless --disable-gpu  --dump-dom  --no-sandbox '%s' >%s\n" ,_wget_html , nodelink->linknew , _wget_html );
				}
				//wget
				else{

					char convert_links[]="--convert-links";
					char url[1000];
					//webserver 方式，通过设定的本地或远程web服务器代理采集信息，主要用于微信、微博等防止采集的网站
					if(ToolsWebServerAll == nodelink->tools ||ToolsWebServerWeb == nodelink->tools && IsWeb == nodelink->web_or_link ){
						//$url = "http://".$ip_port."/webserver?type=link&url=".$link;
						//$url = "http://" . $ip_port . "/webserver?type=info&url=" . $link;
						char link_utf8[1000], link_base64[1000];
						//这里遗留一个问题，base64之前必须是utf8编码，而原始连接可能是utf8或gbk，必须先做编码判断，否则utf8转utf8会出错。目前默认都是utf8，不进行转换，所以会有错。
						//gb_to_utf8(nodelink->linknew , link_utf8);
						strcpy(link_utf8 , nodelink->linknew);

						base64_encode(  link_utf8, link_base64);
						sprintf(url , "http://%s/webserver?type=web&url=%s" ,nodelink->node_web->nodeWQ->webServer , link_base64); //127.0.0.1:6081
						convert_links[0] = '\0';
					}
					else
						strcpy(url , nodelink->linknew);
					nodelink->tools = ToolsWget;
					get_working_wget_baseinfo( nodelink,ThreadInfo->WgetWorkDir,_son_wget_info,_wget_html,wget_html);

					if( '\0' != getproxystr[0])
						sprintf(proxystr , " -e  \"http_proxy=%s\" " ,getproxystr);
					else
						proxystr[0] = '\0';
					// --convert-links 这个参数在采集多层的时候把链接变成相对链接，在采集单个页面时，把页面中的链接全部变成物理链接，很有价值，对我们自己提取页面链接极有帮助
					//限速带宽35M
					//有链接反应的,连接超时，时间在timeout*(tries+1)	-nv
					//--bind-address=63.141.239.123
					if(0 == onewgetLimitRate || nodelink->node_web->nodeWQ->type != IsWeb)//nodelink->node_web->webinfo.type != IsWeb)
						sprintf(str_onewgetLimitRate," ");
					else
						sprintf(str_onewgetLimitRate ,"  --limit-rate=%dk	",onewgetLimitRate);

					sprintf(out_file_str,"	-q	");
					if(strstr( nodelink->linknew, "://dealer.xcar.com.cn")){
							get_cookie_filename("dealer.xcar.com.cn",ThreadInfo->WgetWorkDir , cookie_file );
							sprintf(cookie_str,"--load-cookies=\"%s\" --save-cookies=\"%s\"",cookie_file,cookie_file);
					}
					else
						cookie_str[0] = '\0';

					sprintf(order_standard,"%s	%s	%s %s --timeout=%d	 --tries=1   %s --no-check-certificate	-erobots=off  -Q1m	 %s  --user-agent=\"%s\"		-O %s	  --accept=html,htm,shtml,asp,php,jsp	  \"%s\" \n" ,Mywget,out_file_str,str_onewgetLimitRate,cookie_str ,nodelink->node_web->nodeWQ->WgetTimeOut ,convert_links, proxystr,agent ,_wget_html , url);
				}

				//条件脚本开始语句
				//--------------------------------------
				//	 50828 0.txt
				//	  6871 1.txt
				//	 57699 总用量
				//	 http://center.estar360.com/center/center.php?md5=e517c56ae64cbb4e7f88578be1f7dfdc

				if(2<1 && 0 == nodelink->layer){ // 1 == IfCheckCenter
					//get_center_filename(nodelink->md5,ThreadInfo->WgetWorkDir , center_file );
					sprintf(order_tmp,"wget -q \"%s?md5=%s\" -O %s\n" ,CheckCenterLink,nodelink->md5 ,_wget_html );
					fputs(  order_tmp,FILE_SH);
					//获取查询结果，如果num == 1那么是重复，不采集，如果查询结果不为1,有可能是0或者没有下载成功，那么要采集
					sprintf(order_tmp,"num=`cat %s|awk '{printf $0}' `\n" , _wget_html);
					fputs( order_tmp,FILE_SH);

					sprintf(order_tmp,"if [ \"$num\" = \"1\" ]; then\n");
					fputs(  order_tmp,FILE_SH);
						//sprintf(order_tmp,"echo \" 1\" >> /home/zran/src/manzhua23/1.txt\n" );
						//fputs(  order_tmp,FILE_SH);
						//fputs(  "num=1",FILE_SH);
						sprintf(order_tmp,"mv  %s %s \n" ,_wget_html, wget_html);
						fputs(  order_tmp,FILE_SH);
					//如果查询结果不为1,有可能是0或者没有下载成功，那么要采集
					fputs(  "else\n",FILE_SH);
						//sprintf(order_tmp,"echo \" 0\" >> /home/zran/src/manzhua23/0.txt\n" );
						//fputs(  order_tmp,FILE_SH);
						//标准采集语句
						//--------------------------------------
						fputs(  order_standard,FILE_SH);//******************************

						sprintf(order_tmp,"mv  %s %s \n" ,_wget_html, wget_html);
						fputs(  order_tmp,FILE_SH);
					fputs("fi\n" , FILE_SH);


				}
				//标准采集语句
				//--------------------------------------
				else{
					fputs(  order_standard,FILE_SH);//******************************
					if(1 == ifmove){
						sprintf(order_tmp,"mv  %s %s \n" ,_wget_html, wget_html);
						fputs(  order_tmp,FILE_SH);
					}
				}


				fputs(  "\n",FILE_SH);

				nodelink = nodelink->next;
	 	}
		fclose(FILE_SH);


		//运行SH
		sprintf(order_tmp ,"/bin/sh %s  &",nodeSH->shfilename );
		system(order_tmp);

		//统计信息
		ThreadInfo->LoopThreadSmall.link_download = ThreadInfo->LoopThreadSmall.link_download  + nodeSH->num_wget;
		//if( nodeSH->index > ErrorWaitingQL )
		//{
		ThreadInfo->LoopThreadSmall.sh_add++;
		//}
		update_download_tm(nodeSH->QLWget->front);
		ThreadInfo->LoopBig.sh_working++;
		//pthread_mutex_lock(&mymutex_sh_working);
		//ThreadInfo->nodeWQ->LoopQueue.sh_working++;
		//pthread_mutex_unlock(&mymutex_sh_working);
		nodeSH->working  = SHWorking;
		nodeSH->numcheck = 0;

		//移动到working队列中，返回的是下一个添加弹药的节点
	    nodeSH = move_nodeSH(ThreadInfo->QLTaskSH_waiting,  nodeSH, ThreadInfo->QLTaskSH_working);

	}
	else{
		nodeSH->working  = SHWaiting;
		//nodeSH = nodeSH->next; //没必要
	}
	//clear_working_wget_baseinfo( ThreadInfo   ) ;
	return nodeSH;
}
int fclose_run_all_sh(struct THREADINFO *ThreadInfo )
{

	QNodeSH *nodeSH  ;

	nodeSH = ThreadInfo->QLTaskSH_waiting->front;
	//printf("------------sh_working=%d-----NumSHInThread=%d--\n" ,count_SH(struct QListSH * QLTaskSH, int working),ThreadInfo->LoopBig.sh_working , ThreadInfo->nodeWQ->NumSHInThread );
	while(nodeSH  && ThreadInfo->LoopBig.sh_working < ThreadInfo->nodeWQ->NumSHInThread )//&& nodeSH->next
	{
		// printf("%2d  index=%d  working=%d  %s  nodeSH->num_wget=%d  wget_working_all=%d  \n" ,ThreadInfo->myid, nodeSH->index,nodeSH->working,"all", nodeSH->num_wget ,ThreadInfo->LoopBig.wget_working_all);
		if(nodeSH->working ==  SHAdding){
			//返回的是下一个添加弹药的节点
			nodeSH = fclose_run_a_sh( ThreadInfo , nodeSH );
			continue;
		}
		nodeSH = nodeSH->next;
	}

	return 0;
}
int    if_good_nodesh(QNodeSH *nodeSH)
{

		if(nodeSH->working ==  SHWaiting)
		{
			//nodeSH->FILE_SH = fopen(nodeSH->shfilename, "w");
			//if(nodeSH->FILE_SH == NULL ) {printf("creat sh error [%s]\n",nodeSH->shfilename);return NULL;}
			nodeSH->num_wget = 0;
			nodeSH->numcheck =0;
			nodeSH->working  =  SHAdding ;

		}

		return nodeSH->working;
}
QNodeSH *  find_a_nodeSH_left(QNodeSH * nodeSH_begin, QNodeSH *nodeSH_end)
{
	//队列开始，到某个节点之前结束
	QNodeSH *nodeSH =nodeSH_begin;
	while(nodeSH  && nodeSH != nodeSH_end  )  //如果队列中只有一个节点，那么在find_a_nodeSH_right中就解决了
	{
		//发现一个可以装弹的sh节点
		if(SHAdding  ==if_good_nodesh(nodeSH) ) return nodeSH;
		nodeSH = nodeSH->next;
	}

	return NULL;
}
QNodeSH *  find_a_nodeSH_right( QNodeSH *nodeSH_begin  )
{
	//某个节点开始，到队列尾部
	QNodeSH *nodeSH =nodeSH_begin;
	while(nodeSH   )
	{
		//发现一个可以装弹的sh节点
		if(SHAdding  ==if_good_nodesh(nodeSH) ) return nodeSH;
		nodeSH = nodeSH->next;
	}

	return NULL;
}

QNodeSH *  find_a_nodeSH_one( QNodeSH *nodeSH_begin  ){
	//printf("nodeSH->working = %d\n",nodeSH_begin->working);
	QNodeSH *nodeSH =nodeSH_begin;
	while(nodeSH   )  {
		//发现一个可以装弹的sh节点
		if(0 == nodeSH->index && SHAdding  ==if_good_nodesh(nodeSH) )
			return nodeSH;
		nodeSH = nodeSH->next;
	}
	return NULL;
}

QNodeSH * find_nodeSH_all( struct QListSH *QLTaskSH ,QNodeSH *nodeSH , struct THREADINFO *ThreadInfo ,int type )
{
	if(ThreadInfo->LoopBig.sh_working   <  ThreadInfo->nodeWQ->NumSHInThread)
	{
		//微信特殊处理，微信搜索web只添加到0号sh队列中，微信信息下载放到其他队列，这样配合效率高20180909********************************
		if(IsWeiXin == ThreadInfo->nodeWQ->type  && IsWeb == type){
			nodeSH = QLTaskSH->front;
			QNodeSH *nodeSH_new;
			if(nodeSH_new = find_a_nodeSH_one( nodeSH )) return nodeSH_new;
		}
		//公共处理
		else{
			if(NULL == nodeSH) nodeSH = QLTaskSH->front;//**************************

			QNodeSH *nodeSH_new;
			//寻找队列剩余节点中是否有可以添加的节点
			if(nodeSH_new = find_a_nodeSH_right(  nodeSH )) return nodeSH_new;

			//从队列开始找是否有可以添加的节点
			if(nodeSH_new = find_a_nodeSH_left( QLTaskSH->front,  nodeSH)) return nodeSH_new;
		}

	}
	return NULL;
}
int check_SH(struct QListSH *QLTaskSH ){
	QNodeSH *nodeSH=QLTaskSH->front;
	while(nodeSH  )  //&& nodeSH != QLTaskSH->end
	{

		if(SHWaiting != nodeSH->working ) // nodeSH->working  >  SHWaiting
		{
			return 1;
		}
		nodeSH = nodeSH->next;
	}

	return 0;
}
int count_SH(struct QListSH *QLTaskSH ,int working )
{

	QNodeSH *nodeSH=QLTaskSH->front;
	 int num=0;

	while(nodeSH  )  //&& nodeSH != QLTaskSH->end
	{

		//if(nodeSH->working == working   )
		//{
			num++;
		//}
		nodeSH = nodeSH->next;
	}

	return num;
}
/*
struct QNodeSH *   add_link_to_sh(struct QList *QLWgetWaiting ,struct QNodeSH *nodeSH, struct THREADINFO *ThreadInfo  )
{
		//把1个节点加入某个sh的节点中
 		struct QNodeLink* nodelink= QLWgetWaiting->front;
		if(nodelink )
		{
			Move_node( QLWgetWaiting , nodeSH->QLWget, ThreadInfo);

			ThreadInfo->LoopThreadSmall.wget_new_run++;
			ThreadInfo->LoopBig.wget_working_all++;
			ThreadInfo->LoopBig.wget_waiting_all--;
			nodeSH->num_wget++;
			nodelink->ifdownloaded = 1;

			//关闭SH文件，并运行，还要加入SH队列中，队列中有一个大于1层的链接就马上写文件，不再添加新链接
			if(   nodeSH->num_wget >=  ThreadInfo->nodeWQ->NumWgetInSH
				|| IsWeb ==nodelink->web_or_link  && IsWeb != nodelink->node_web->nodeWQ //使用代理服务器节点一律只加一个wget
				//|| IsWeb == nodelink->web_or_link && ( nodelink->layer > 1 || ThreadInfo->num_wget_depth >0) //发现一个采集多层次的，且是个web,************ //如果线程中有多层采集了，那么sh中只能添加一个web就必须运行
				//|| nodelink->web_or_link == IsWeb &&   nodelink->layer > 1  //发现一个采集多层次的，且是个web,************
				//|| nodelink->web_or_link == IsWeb &&   ThreadInfo->num_wget_depth >0   //如果线程中有多层采集了，那么sh中只能添加一个web就必须运行
				)  //|| ThreadInfo->num_wget_waiting_all < 1
			{
				//printf("nodeSH->num_wget=%d\n",nodeSH->num_wget);
				nodeSH = fclose_run_a_sh(ThreadInfo ,nodeSH );
				//nodeSH= move_nodeSH(ThreadInfo->QLTaskSH_waiting,  nodeSH, ThreadInfo->QLTaskSH_working);
				//nodeSH->working = 3;
				return nodeSH;
			}
		}
		return nodeSH->next;
}
*/
struct QNodeSH *   add_nodelink_to_sh(struct QNodeLink* nodelink ,struct QNodeSH *nodeSH   )
{
		//把1个节点加入某个sh的节点中
		if(nodelink ){
			InsertQLWorking(nodeSH->QLWget, nodelink);

			nodeSH->num_wget++;
			//printf("%d/%d\n" ,nodeSH->num_wget, nodelink->threadinfo->nodeWQ->NumWgetInSH);
			//printf("nodelink->threadinfo->nodeWQ->type=%d\n",nodelink->threadinfo->nodeWQ->type);
			//关闭SH文件，并运行，还要加入SH队列中，队列中有一个大于1层的链接就马上写文件，不再添加新链接
			if(   nodeSH->num_wget >=  nodelink->threadinfo->nodeWQ->NumWgetInSH
				//|| IsWeb ==nodelink->web_or_link  &&    nodelink->threadinfo->nodeWQ->type>-1 // IsWeb != nodelink->node_web->nodeWQ->type //使用代理服务器节点一律只加一个wget
				|| nodelink->node_proxy
				//|| IsWeb == nodelink->web_or_link && ( nodelink->layer > 1 || ThreadInfo->num_wget_depth >0) //发现一个采集多层次的，且是个web,************ //如果线程中有多层采集了，那么sh中只能添加一个web就必须运行
				//|| nodelink->web_or_link == IsWeb &&   nodelink->layer > 1  //发现一个采集多层次的，且是个web,************
				//|| nodelink->web_or_link == IsWeb &&   ThreadInfo->num_wget_depth >0   //如果线程中有多层采集了，那么sh中只能添加一个web就必须运行
				//|| IsWeiXin == nodelink->threadinfo->nodeWQ->type && IsWeb ==nodelink->web_or_link //微信强制只在sh中添加一个任务，在设置参数时，sh中时多个，这样保证，解析的微信真实信息可以快速下载
			  )  //|| ThreadInfo->num_wget_waiting_all < 1
			{
				//printf("%d nodeSH->num_wget=%d\n",nodelink->threadinfo->myid,nodeSH->num_wget ,nodelink->node_web->nodeWQ );
				nodeSH = fclose_run_a_sh(nodelink->threadinfo ,nodeSH );
				return nodeSH;
			}
		}
		return nodeSH->next;
}


int maxloop =0;
int check_nodeSH(struct QNodeSH *nodeSH)
{
	struct QNodeLink* nodewget=nodeSH->QLWget->front;
	while(nodewget)
	{
		if(nodewget->layer > 1) return 1;
		nodewget = nodewget->next;
	}
	return 0;
}
#define IsEnd	-1
#define IsNotOK	0
#define IsOK	1
int   find_a_nodeWeb( struct THREADINFO *ThreadInfo ,struct QNodeSH *nodeSH){
	int bad=0,myreturn = IsEnd;
	//QNodeWeb *  node_web = ThreadInfo->node_web_new;
	while(  ThreadInfo->node_web_new && (ThreadInfo->LoopBig.wget_depth < 1  || ThreadInfo->node_web_new->layer < 2   ) )// && ThreadInfo->node_web->index  <=  ThreadInfo->nodeWQ->QLWeb->end->index)  || ThreadInfo->LoopBig.wget_working_all ==1 &&
	{
			//强制微信同一时间只能有2个sh工作，这样避免被封ip
			if(2<1 && IsWeiXin == ThreadInfo->nodeWQ->type && ThreadInfo->nodeWQ->num_web_working >1)
				break;
		 	//printf("%2d index=%2d/%2d   num_nodelink_working=%3d / %d     download=%d   loop=%3d/%3d\n",ThreadInfo->myid,ThreadInfo->node_web_new->index,ThreadInfo->nodeWQ->index,ThreadInfo->node_web_new->num_nodelink_working,ThreadInfo->loop_thread,ThreadInfo->node_web_new->download ,ThreadInfo->node_web_new->loop_web,  ThreadInfo->loop_thread);
			pthread_mutex_lock(&mymutex_web);
		    if(  0 ==  ThreadInfo->node_web_new->num_nodelink_working && 0 ==  ThreadInfo->node_web_new->mylock //被别的线程占用
				&& 	ThreadInfo->node_web_new->download > 0            //不需要下载了
				&& ThreadInfo->node_web_new->loop_web <  ThreadInfo->loop_thread//这圈已经下载了***********************************
				//&& time((time_t *) NULL) - ThreadInfo->node_web_new->tm_last_download >  ThreadInfo->nodeWQ->IntervalTimeWeb

		     	)
		    	{
		    		ThreadInfo->node_web_new->mylock = ThreadInfo->myid;
					myreturn= IsOK;
					pthread_mutex_unlock(&mymutex_web);
					break;
		    	}
			pthread_mutex_unlock(&mymutex_web);
			ThreadInfo->node_web_new =  ThreadInfo->node_web_new->next;
	}
	//这个时候node_web==NULL
	return myreturn ;
}

QNodeLink* find_a_nodeLink(MYSQL *conn  ,struct THREADINFO *ThreadInfo)
{
		//寻找可以下载的节点，若节点不符合要求，就删除，符合条件移出
		int ifdownload;
		//
		QNodeLink* nodelink;
		while(nodelink=DeleteQLfront(ThreadInfo->QLWgetWaiting))
		{
				ThreadInfo->LoopBig.wget_waiting_all--;
				//nodelink = ;
				if(check_a_nodeLink( conn, nodelink))
				{
					//*******************************************
					//pthread_mutex_lock(&mymutex_wget_waiting_all);
					//ThreadInfo->nodeWQ->LoopQueue.wget_waiting_all--;
					//pthread_mutex_unlock(&mymutex_wget_waiting_all);
					nodelink->node_proxy = ThreadInfo->node_proxy;
					return nodelink;// DeleteQLfront(ThreadInfo->QLWgetWaiting);
				}
				else
				{
					DeleteQLWget_QLWgetWaiting(nodelink) ;
				}
		}
		//pthread_mutex_unlock(&mymutex_wget_waiting_all);
		return NULL;

}

QNodeSH *add_link(MYSQL *conn    ,struct QListSH *QLTaskSH_waiting ,struct THREADINFO *ThreadInfo){
	struct QNodeLink * nodelink;
	QNodeSH *nodeSH = QLTaskSH_waiting->front;
	while(nodeSH = find_nodeSH_all(QLTaskSH_waiting , nodeSH ,ThreadInfo,IsLink)){
		//寻找代理服务器
		//if(2<1 &&  IsWeiXin == ThreadInfo->nodeWQ->type ){  //ThreadInfo->nodeWQ->index_proxy !=  NotUseProxy   &&
		if( Connection_proxy_all == ThreadInfo->nodeWQ->Connection){
	      	ThreadInfo->node_proxy = find_proxy( QLProxy , ThreadInfo->node_proxy , ThreadInfo->nodeWQ->index_proxy  );
			if(NULL == ThreadInfo->node_proxy){
				printf("add_link getproxynodenow error myid =%d   index_proxy=%d   [%s]\n" , ThreadInfo->myid, ThreadInfo->nodeWQ->index_proxy, ThreadInfo->nodeWQ->web);
				return nodeSH;
			}
	    }
		else
			ThreadInfo->node_proxy = NULL;


		if(nodelink = find_a_nodeLink(  conn,   ThreadInfo))
			nodeSH = add_nodelink_to_sh(  nodelink,   nodeSH);
		else{
			//代理取到，但没有合适的链接，那么要释放代理
			if(ThreadInfo->node_proxy)
				ThreadInfo->node_proxy->good[ThreadInfo->nodeWQ->index_proxy]--;// = proxy_free;
			break;
		}
	}
	return  nodeSH;
}



int add_web(MYSQL *conn ,QNodeSH *nodeSH,struct THREADINFO *ThreadInfo)
{

	//----------------------------------------------------------------
	//添加网址
	//----------------------------------------------------------------
	//--------------------------------------------------------------------
	int  node_retrun,ifgetproxy;

	QNodeWeb *node_web;
	while(nodeSH = find_nodeSH_all(ThreadInfo->QLTaskSH_waiting, nodeSH ,ThreadInfo,IsWeb) ){
		 	ifgetproxy = 1;
			while( 1 ) {

				//如果网址节点没到时间，那么它后边的节点也不会到时间，就别取了，直接中断，必须中断，不能跳过找下边的节点
				//if( time((time_t *) NULL) - ThreadInfo->node_web->last_wget_downlaod_tm <  ThreadInfo->nodeWQ->IntervalTimeWeb) break;

				//如果队列中有大于1层的节点，且当前节点也大于1层，必须中断，不能跳过找下边的节点
				//if( ThreadInfo->num_wget_depth  >1 && ThreadInfo->node_web->layer >1) break;//有
				//if(ThreadInfo->node_web->layer <2  ||   ThreadInfo->num_wget_depth  < 1  )  //层数判断
				//{
				//sprintf(sql , "UPDATE `manzhua`.`web_md5` SET `mylock`='%d'  ,`order`='%d' WHERE  `mylock` <1  AND `type`=%d  %s AND `download`>0 AND `loop`<'%d'  ORDER BY  `web_md5`.`tm` ASC , `web_md5`.`loop` ASC    LIMIT 1" , webinfo->myid,order,webinfo->type,tinytypestr,webinfo->loop);
				//ThreadInfo->node_web->mylock = ThreadInfo->myid;

				// 1 、先获取代理服务器
				//if(0 == get_proxy_manage(nodelink,proxystr)           )
				if( NotUseProxy != ThreadInfo->nodeWQ->index_proxy && 1 == ifgetproxy){ //IsWeb != ThreadInfo->nodeWQ->type
			      	ThreadInfo->node_proxy = find_proxy( QLProxy , ThreadInfo->node_proxy , ThreadInfo->nodeWQ->index_proxy  );
					if(NULL == ThreadInfo->node_proxy){
						printf("add_web getproxynodenow error myid =%d   index_proxy=%d   [%s]\n" , ThreadInfo->myid, ThreadInfo->nodeWQ->index_proxy, ThreadInfo->nodeWQ->web);
						return 0;
					}
			    }
				else
					ThreadInfo->node_proxy = NULL;

				// 2、提取网址
				node_retrun =  find_a_nodeWeb( ThreadInfo ,nodeSH);
				//printf("add_web myid= %d     node_retrun= %d   \n",ThreadInfo->myid,node_retrun );
				if(node_retrun == IsOK){
					node_web= ThreadInfo->node_web_new;
				}
				else if(node_retrun == IsNotOK){
					if(ThreadInfo->node_proxy) ThreadInfo->node_proxy->good[ThreadInfo->nodeWQ->index_proxy]--;// = proxy_free;
					return 0;
				}
				else if(node_retrun == IsEnd){
					if(ThreadInfo->node_proxy) ThreadInfo->node_proxy->good[ThreadInfo->nodeWQ->index_proxy]--;// = proxy_free;
					return 0;
				}

				// 3、建立采集节点
				QNodeLink* node_link = create_new_node_link( ThreadInfo, node_web,node_web->layer,IsWeb,node_web->download ,0,0,node_web->loop_web);
				node_link->query_return  = lock_link_md5( conn, ThreadInfo ,  node_link);
				if(LinkError == node_link->query_return )
					return 0;
				else if(Link_Unlock == node_link->query_return ) {
					//更改download
					node_web->download = node_link->download_database;

					freeQNodeLink(node_link);
					//释放网站
					unlock_web_md5 ( node_web ,ThreadInfo->loop_thread,0 );

					ThreadInfo->node_web_new=  ThreadInfo->node_web_new->next;
					ifgetproxy = 0;
					continue;
				}
				else{
					//添加网站任务成功

					//统计线程信息
					ThreadInfo->LoopThreadSmall.web_add++;
					ThreadInfo->nodeWQ->num_web_working++;
					//InsertQLWaiting(ThreadInfo->QLWgetWaiting,node_link);

					//nodeSH= add_link_to_sh(ThreadInfo->QLWgetWaiting,  nodeSH ,ThreadInfo);

					node_link->node_proxy = ThreadInfo->node_proxy;
					InsertQL_tongji(node_link,iswroking);
					ThreadInfo->tm_add_web_last =  time((time_t *) NULL) ;
					nodeSH= add_nodelink_to_sh(node_link,  nodeSH );
					ThreadInfo->node_web_new=  ThreadInfo->node_web_new->next;
					break;
				}
			}
	}

	return 0;
}
int Create_and_run_sh_file(  struct THREADINFO *ThreadInfo )
{
	QNodeSH *nodeSH;
	//----------------------------------------------------------------
	//添加链接
	//----------------------------------------------------------------
	nodeSH = add_link(ThreadInfo->conn   ,ThreadInfo->QLTaskSH_waiting, ThreadInfo); //nodeSH返回一个当前可以添加的节点


	//----------------------------------------------------------------
	//添加网址
	//----------------------------------------------------------------
	add_web(ThreadInfo->conn   ,nodeSH,ThreadInfo);

	//----------------------------------------------------------------
	//运行采集sh
	//----------------------------------------------------------------
	fclose_run_all_sh(  ThreadInfo );

	return 0;
}
int check_file_content(char *file ,char *str){
	int myreturn = 0;
	char *filestr = file2strzran(file);
	if(NULL == filestr )
		myreturn = 0;
	else if(0 == strcmp(filestr ,  str))
		myreturn = 1;
	else
		myreturn = 0;
	free(filestr);
	return myreturn;
}

int Do_WgetQLWorking(    struct THREADINFO *ThreadInfo)
{
		MYSQL *conn =ThreadInfo->conn;
		/*
			st_atime 文件最近一次被存取或被执行的时间，一般只有在用mknod、utime、read、write与tructate时改变。
			st_mtime 文件最后一次被修改的时间，一般只有在用mknod、utime和write时才会改变
			st_ctime i-node最近一次被更改的时间，此参数会在文件所有者、组、权限被更改时更新先前所描述的st_mode 则定义了下列数种情况

			Access: 2012-05-09 11:20:54.410743549 +0800
			Modify: 2012-05-09 17:54:57.979374772 +0800
			Change: 2012-05-09 17:54:57.979374772 +0800

			access time是文档最后一次被读取的时间。因此阅读一个文档会更新它的access时间，但它的modify时间和change时间并没有变化。cat、more 、less、grep、sed、tail、head这些命令都会修改文件的access时间。
			modify time是文本本身的内容发生了变化。[文档的modify时间也叫时间戳(timestamp).]
			change time是文档的索引节点(inode)发生了改变(比如位置、用户属性、组属性等)；

			检查某个进程是否存在，如果aaa.txt文件大小大于0，就是存在，否则是不存在
			 ps -ef| grep _129206_0_1_4217379985_1339950223_2_1_91117a2f679c4803d6eea29879ed8e62|grep -v grep >aaa.txt
		*/
	int nowHour = getNow(NowHour);
	//printf("nowHour = %d\n" , nowHour);
	int begin=time((time_t *) NULL);
	//printf("%2d Do_WgetQLWorking  (%d/%d) begin\n" , ThreadInfo->myid,ThreadInfo->num_sh_working ,ThreadInfo->num_sh_needwork);
	int  dodo;
	struct stat tbuf,tbuf_wget_html;//l,tbuf_wget_info;
	//char wget_html[200],_wget_html[200],_wget_info[200],__wget_titlelink[200];
	unsigned  int  used_time;

	QNodeLink* node_wget ;// 当前节点
	QNodeSH *nodeSH= ThreadInfo->QLTaskSH_working->front    ; //指向第一个节点

	while(nodeSH && ThreadInfo->LoopBig.sh_working > 0)//&&  &&  ThreadInfo.loop_wgetworking_num < ThreadWgetMaxnum
	{
		//printf("%d   %d  (%d/%d)\n" , i,nodeSH->working     , ThreadInfo->num_sh_working ,ThreadInfo->num_sh_needwork);
		if(SHWorking != nodeSH->working   ) {
			printf("nodeSH->working=%d\n",nodeSH->working);
			nodeSH = nodeSH->next;
			continue;
		}
		//else if(nodeSH->working ==2 ) {printf("dddddddddddddddddddddddddddddddddddddddddddd\n"); break;}

		nodeSH->numcheck++;
		//只处理本圈的链接，新增加的链接不处理 ??????
		//队列处理中如果已经发现有ThreadWgetMaxnum个在工作了，那就中断检查，否则大量新增链接又没有wget额度，浪费检查资源。
		//printf("%d\n" , CountQL(ThreadInfo->QLWgetWorking));
		node_wget= nodeSH->QLWget->front; //指向第一个节点
		while(node_wget  && node_wget->begin_wget_download_tm < time((time_t *) NULL))
		{
				//node_wget->numcheck++;
				//任务类型是下载中
				//检查文件是否下载完毕，下载完了，就进行连接处理，新文件就写文件处理，需要二级采集的就加入队列中,下载完毕的返回1，还没处理完的返回0

				// 2、提取_wget_info文件，文件大小很重要，大于0的是下载完的，小于1的正在下载的或已经是死链接的。
				get_working_wget_baseinfo(  node_wget,ThreadInfo->WgetWorkDir,ThreadInfo->_son_wget_info,ThreadInfo->_wget_html,ThreadInfo->wget_html);

				//sprintf(__wget_titlelink,"%s__%s",ThreadInfo->WgetWorkDir,node_wget->md5);
				if(    stat (ThreadInfo->wget_html , &tbuf_wget_html) == 0)   //文件下载成功
				{
						node_wget->ifdownloaded = 1;
						node_wget->loop_link++; //必须是++，不能用ThreadInfo->loop_thread,只是作为father用，不写库
						if(tbuf_wget_html.st_size <10   )  // myerror = 2; //这种文章不要
						{
							//文件下载错误完毕
							node_wget->download_link =  Download_TooSmall ;//-5; //文件太小 //************************
							checkConnection(node_wget->node_web->nodeWQ);

						}
						else if(tbuf_wget_html.st_size >MaxWebSize   )
						{
							//文件下载错误完毕
							node_wget->download_link = Download_TooBig;//-102; //文件太大//************************
						}
						else
						{
							//文件下载正常完毕
							ThreadInfo->LoopThreadSmall.link_download_ok++; //很重要
							if(  1 == node_wget->layer && 							//必须是倒是1层页面
								 tbuf_wget_html.st_size == node_wget->size_last &&  //2次采集页面大小一样
								 nowHour  > 6  										//在每日0-6点之间更新这类网页的下级页面链接 20180920
							){
								//下载倒数第一层，如果页面大小没变化，就不处理，认为是没有新连接 ,
								//有问题，如果长时间不更新这个页面的链接，数据库清理时就会删除链接，这个页面再更新时，会采集所有下级页面，提供48小时的清理缓冲，大多数页面会好些
								//补丁，在每日0-6点之间更新这类网页的下级页面链接
								//printf("same size   node_wget->layer =%d   (%d/%d)\n" , node_wget->layer ,tbuf_wget_html.st_size , node_wget->size_last );

							}
							else
								do_wget_downloaded_file(conn,     node_wget   ,  ThreadInfo ); // 1;//处理成功
							node_wget->size_last	= tbuf_wget_html.st_size ;
							node_wget->download_link = Download_OKTrue;//************************
						}

						DeleteQLWget_QLWgetSH(conn,  nodeSH->QLWget ,ThreadInfo  ) ;
						remove(ThreadInfo->wget_html );


				}
				else //文件还未下载完
				{
						//检查文章下载了多长时间
						dodo=0;
						used_time = time((time_t *) NULL) - node_wget->begin_wget_download_tm  ;
						if( used_time >120)
						{
								node_wget->download_link = Download_Timeout; //文件超时
								printf("1--%2d   %s   used_time=%d \n" ,ThreadInfo->myid ,ThreadInfo->_wget_html  ,used_time);
								dodo = 1;
						}
						else
						{
								if( stat (ThreadInfo->_wget_html,&tbuf) ==0 ) // access( ThreadInfo->_wget_html , F_OK ) == 0   &&
								{
									if( tbuf.st_size  >MaxWebSize )
									{
										//这种超长时间的的链接，可能变成了死链接
										node_wget->download_link = Download_TooBig;// -103; //文件太大//************************
										printf("2--%2d   %s  tbuf.st_size =%d \n",ThreadInfo->myid  ,ThreadInfo->_wget_html ,tbuf.st_size);
										dodo = 1;
									}
									else
									{
										if(  used_time >60 &&  tbuf.st_size  < 1)
										{
											node_wget->download_link = Download_TooSmall;//-2;//************************
											printf("3--%2d  %s  tbuf.st_size =%d  used_time=%d \n" ,ThreadInfo->myid,ThreadInfo->_wget_html ,tbuf.st_size ,used_time);
											dodo =  1;
										}
										else
										{
											//正常下载中,其他节点没有必要再检查了
											dodo=0;
										}
									}
								}
								else
								{
									//情况不明的错误，待查,好像是由于磁盘操作负荷太大引起的。处理错误的sh大量出现，原因不明,或者rename了，在cpu占用多时发生几率高
									// 1 基本可以确定是多线程、多进程在分配cpu资源时，恰巧，刚执行到这,文件被rename,
									// 2 某个wget命令被杀死了，他的继续者还没来及运行，也会出现这个错误
									if(used_time> 30)
									{
										node_wget->download_link = Download_Timeout;
										dodo =  1;
									}
									else
										dodo=0;

									printf("----------NO myid=%2d  nodeSH->index=%d %s  tbuf.st_size =%d  used_time=%d numcheck=%d %s\n" ,ThreadInfo->myid,nodeSH->index ,ThreadInfo->_wget_html ,tbuf.st_size ,used_time,nodeSH->numcheck,nodeSH->shfilename );
									//sleep(10000);

								}
						}



						if(dodo == 1){
							checkConnection( node_wget->node_web->nodeWQ);
							node_wget->ifdownloaded = 1;
							node_wget->loop_link++; //必须是++，不能用ThreadInfo->loop_thread,只是作为father用，不写库
							kill_process(ThreadInfo->_son_wget_info  );
							DeleteQLWget_QLWgetSH(conn,   nodeSH->QLWget ,ThreadInfo ) ;
							remove(ThreadInfo->_wget_html);
							remove(ThreadInfo->wget_html);

						}

						break;

				}

				node_wget =  nodeSH->QLWget->front;
		}

		if(nodeSH->QLWget->front == NULL)
		{
			nodeSH->working = SHWaiting;
			nodeSH->num_wget = 0;
			nodeSH->numcheck =0;
			ThreadInfo->LoopBig.sh_working--;
			//pthread_mutex_lock(&mymutex_sh_working);
			//ThreadInfo->nodeWQ->LoopQueue.sh_working--;
			//pthread_mutex_unlock(&mymutex_sh_working);
			//移动到等待队列中
			nodeSH = move_nodeSH(ThreadInfo->QLTaskSH_working,   nodeSH,  ThreadInfo->QLTaskSH_waiting);
			continue;
		}

		nodeSH = nodeSH->next;

	}
	clear_working_wget_baseinfo( ThreadInfo ) ;
	//printf("%2d  Do_WgetQLWorking  (%d/%d) end   %d\n" , ThreadInfo->myid,  ThreadInfo->num_sh_working ,ThreadInfo->num_sh_needwork ,time((time_t *) NULL)-begin);
	return 0;
}
int init_LoopThreadSmall(struct THREADINFO *ThreadInfo)
{
	ThreadInfo->LoopThreadSmall.web_add= 0;
	ThreadInfo->LoopThreadSmall.link_parse = 0;
	ThreadInfo->LoopThreadSmall.wget_new_run = 0;
	ThreadInfo->LoopThreadSmall.link_download_ok   = 0;
	ThreadInfo->LoopThreadSmall.link_download   = 0;

	ThreadInfo->LoopThreadSmall.sh_add = 0;
	ThreadInfo->LoopThreadSmall.tm_work_begin=  time((time_t *) NULL);

}
int init_LoopThread(struct THREADINFO *ThreadInfo)
{
	ThreadInfo->LoopThread.web_add= 0;
	ThreadInfo->LoopThread.link_parse = 0;
	ThreadInfo->LoopThread.link_parse_new = 0;
	ThreadInfo->LoopThread.wget_new_run = 0;
	ThreadInfo->LoopThread.link_download_ok   = 0;
	ThreadInfo->LoopThread.link_download   = 0;
	ThreadInfo->LoopThread.link_insert= 0;

	ThreadInfo->LoopThread.link_okwrited =0;
	ThreadInfo->LoopThread.link_bad =0;
	ThreadInfo->LoopThread.sh_add = 0;

	ThreadInfo->LoopThread.tm_work_begin=  time((time_t *) NULL);
	ThreadInfo->node_web_new= ThreadInfo->nodeWQ->QLWeb->front;


	//升级,必须跳动升级，否则遇到大队列，空转一圈很耗费资源
	pthread_mutex_lock(&mymutex_loop_thread_max);
	ThreadInfo->loop_thread ++;
	if(ThreadInfo->loop_thread >  ThreadInfo->nodeWQ->loop_thread_max)
		ThreadInfo->nodeWQ->loop_thread_max = ThreadInfo->loop_thread  ;
	else
		ThreadInfo->loop_thread = ThreadInfo->nodeWQ->loop_thread_max;
	pthread_mutex_unlock(&mymutex_loop_thread_max);

}

int init_LoopQueue(struct QNodeWebQueue *nodeWQ ,int num_web_valid)
{

	nodeWQ->LoopQueue.web_add= 0;
	nodeWQ->LoopQueue.link_parse = 0;
	nodeWQ->LoopQueue.wget_new_run = 0;
	nodeWQ->LoopQueue.link_download_ok  = 0;
	nodeWQ->LoopQueue.link_download   = 0;
	nodeWQ->LoopQueue.link_okwrited= 0;
	nodeWQ->LoopQueue.tm_work_begin  = time((time_t *) NULL);

	nodeWQ->loop_WQ++;
	nodeWQ->num_web_valid =  num_web_valid;
	nodeWQ->num_web_working = 0;
	nodeWQ->LoopQueue.wget_waiting_all = 0;
	nodeWQ->LoopQueue.wget_working_all = 0;
	nodeWQ->LoopQueue.sh_working= 0;
	nodeWQ->LoopQueue.wget_depth =0;
}

int init_LoopBig(struct THREADINFO *ThreadInfo)
{
	if(BigLoop == 1)
		ThreadInfo->loop_thread= 0;
	else
		ThreadInfo->loop_thread= 1;

	ThreadInfo->nodeWQ->loop_thread_max = ThreadInfo->loop_thread;

	ThreadInfo->node_proxy = NULL;
	ThreadInfo->node_web_new= ThreadInfo->nodeWQ->QLWeb->front;

	ThreadInfo->LoopBig.wget_working_all = 0;
	ThreadInfo->LoopBig.sh_working = 0;
	ThreadInfo->LoopBig.wget_waiting_all= 0;
	ThreadInfo->LoopBig.wget_depth=0;
	ThreadInfo->CreatDir.index=0;
	ThreadInfo->LoopBig.link_bad = 0;
	ThreadInfo->LoopBig.link_okwrited =0;
	ThreadInfo->LoopBig.link_okwrited_total =0;

	sprintf(ThreadInfo->WgetWorkDir , "%s%d/" , Savedir,ThreadInfo->myid);

}


int init_ThreadInfo(int myid ,struct THREADINFO *ThreadInfo,struct MYNUM *Num )
{

	int i;
	ThreadInfo->myid = myid;
	ThreadInfo->node_link_index = 0;
	//锁定队列中的线程
	QNodeWebQueue* nodeWQ;
	nodeWQ =QLWebAll->front;
	while(nodeWQ  )
	{
		if(nodeWQ->myid_begin <= myid && myid <  nodeWQ->myid_begin +  nodeWQ->num_thread )
		{
			ThreadInfo->nodeWQ = nodeWQ; //new
			if(nodeWQ->myid_begin == myid) init_LoopQueue( nodeWQ,nodeWQ->num_web);

			//采集队列有个线程的动态数组
			int arraySize = (nodeWQ->threadsNum+1 )*sizeof(struct THREADINFO*);
			nodeWQ->threads  =(struct THREADINFO **) realloc(nodeWQ->threads , arraySize);
			nodeWQ->threads[nodeWQ->threadsNum] = ThreadInfo;
			nodeWQ->threadsNum++;

			break;
		}
		nodeWQ=nodeWQ->next;
	}

	//init_LoopThreadSmall( ThreadInfo);
	//init_LoopQueue( ThreadInfo);
	init_LoopBig( ThreadInfo);
	init_LoopThread( ThreadInfo);

	ThreadInfo->QLWgetWaiting=(struct QList*)malloc(sizeof(struct QList));
	InitQL(ThreadInfo->QLWgetWaiting);   //初始化这个队列


	//ThreadInfo->QLWgetWaiting_error=(struct QList*)malloc(sizeof(struct QList));
	//InitQL(ThreadInfo->QLWgetWaiting_error);   //初始化这个队列


	//printf("%d---------------------------%d\n" , ThreadInfo->myid,ThreadInfo->nodeWQ->NumSHInThread);
	ThreadInfo->QLTaskSH_waiting=(QListSH*)malloc(sizeof(QListSH));
	InitQLSH(ThreadInfo->QLTaskSH_waiting);   //初始化这个队列

	for(i = 0 ; i < ThreadInfo->nodeWQ->NumSHInThread;i++){
		InsertQLTaskSHnew(ThreadInfo->QLTaskSH_waiting ,i,ThreadInfo);
	}
	ThreadInfo->QLTaskSH_working=(QListSH*)malloc(sizeof(QListSH));
	InitQLSH(ThreadInfo->QLTaskSH_working);   //初始化这个队列



	//InsertQLThread(nodeWQ->QLThread, ThreadInfo);
	//ThreadInfo->node_thread_WQ = nodeWQ->QLThread->end;//指向自己

	ThreadInfo->tm_add_web_last =  time((time_t *) NULL) ;
	return 0;
}
int check_web_loop(  struct THREADINFO *ThreadInfo)
{
	// 1、检查队列是否够升级条件
	int num_web_valid =0 ,ifcheck=1;
	QNodeWeb *node_web =  ThreadInfo->nodeWQ->QLWeb->front;
	while(node_web)
	{
		 //printf("%d index=%2d loop_web=%4d/%3d download= %2d working=%d [%s]\n",ThreadInfo->myid,node_web->index ,node_web->loop_web ,ThreadInfo->nodeWQ->loop_WQ,node_web->download,node_web->num_nodelink_working,node_web->link);
		if(node_web->download > Download_Line )
		{

			if(1 == ifcheck &&  node_web->loop_web < ThreadInfo->nodeWQ->loop_WQ)
			{
				char buf[500],buflink[500];
				if(NULL == node_web->linkkw)
					sprintf(buflink,"NULL");
				else
					sprintf(buflink,"%s", node_web->linkkw);
				sprintf(buf,"check :%2d index=%2d loop_web=%4d/%3d download= %2d working=%d mylock=%d [%d][%s]",ThreadInfo->myid,node_web->index ,node_web->loop_web ,ThreadInfo->nodeWQ->loop_WQ,node_web->download,node_web->num_nodelink_working,node_web->mylock,node_web->layer,buflink);
				Recordwork(buf,Recordworkfile);
				printf("%s\n",buf);

				ifcheck=0;//return 0;

			}


			num_web_valid++;
		}
		node_web = node_web->next;
	}

	if(0 == ifcheck)
	{
		ThreadInfo->nodeWQ->num_web_valid =  num_web_valid;
		return 0;
	}


	// 2、显示队列升级信息
	char buf[500];
	struct QNodeWebQueue *nodeWQ = ThreadInfo->nodeWQ;
	int usertime = time((time_t *) NULL)-nodeWQ->LoopQueue.tm_work_begin;
	sprintf(buf,"nodeWQ:%2d /%d/ (%d/%s)  usetime=%4d web=%4d/%d/%d  thread=(%2d / %2d loop)(%d/%d)\n" ,
		//WQbase
		nodeWQ->index,nodeWQ->loop_WQ ,nodeWQ->type,nodeWQ->web,
		//usetime
		usertime,
		//web
		nodeWQ->LoopQueue.web_add ,nodeWQ->num_web_valid,nodeWQ->num_web,
		ThreadInfo->myid,ThreadInfo->loop_thread,
		nodeWQ->LoopQueue.tm_work_begin,ThreadInfo->LoopThread.tm_work_begin
		);
	Recordwork(buf,Recordworkfile);
	printf("%s\n",buf);


	// 3、统计清零
	init_LoopQueue( ThreadInfo->nodeWQ,num_web_valid);

	return 1;
}


int tongji(struct THREADINFO *ThreadInfo  )
{
	//网址处理
	ThreadInfo->LoopThread.web_add = ThreadInfo->LoopThread.web_add + ThreadInfo->LoopThreadSmall.web_add;
	ThreadInfo->LoopThread.link_parse = ThreadInfo->LoopThread.link_parse + ThreadInfo->LoopThreadSmall.link_parse;
	ThreadInfo->LoopThread.wget_new_run = ThreadInfo->LoopThread.wget_new_run + ThreadInfo->LoopThreadSmall.wget_new_run;
	ThreadInfo->LoopThread.link_download_ok = ThreadInfo->LoopThread.link_download_ok + ThreadInfo->LoopThreadSmall.link_download_ok;
	ThreadInfo->LoopThread.link_download= ThreadInfo->LoopThread.link_download + ThreadInfo->LoopThreadSmall.link_download;
	int needsleeptime = 3 - (time((time_t *) NULL) - ThreadInfo->LoopThreadSmall.tm_work_begin) ,index_nodeweb;

	 //显示
	if(2>1)
	{
	 	if(ThreadInfo->node_web_new)
			index_nodeweb = ThreadInfo->node_web_new->index;
		else
			index_nodeweb = -1;

		printf("%2d:%2d L(%2d/%d/%d) sh(%2d.%2d) task(%3d.%3d.%3d.%5d) web(%2d/%4d %5d/%d) link(%3d.%4d.%5d|%4d) s=%d p(%d/%d)\n",

				//base------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
			 	ThreadInfo->nodeWQ->index,ThreadInfo->myid,

				//loop------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
				ThreadInfo->loop_thread , ThreadInfo->nodeWQ->loop_WQ , BigLoop,   //loop

			 	//sh----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
			 	ThreadInfo->LoopThreadSmall.sh_add,ThreadInfo->LoopBig.sh_working ,//ThreadInfo->nodeWQ->LoopQueue.sh_working,//,ThreadInfo->nodeWQ->NumSHInThread,

			 	//task-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
			 	ThreadInfo->LoopThreadSmall.wget_new_run,ThreadInfo->LoopBig.wget_depth , ThreadInfo->LoopBig.wget_working_all,ThreadInfo->LoopBig.wget_waiting_all,//ThreadInfo->nodeWQ->LoopQueue.wget_waiting_all,

			 	//web-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
			 	ThreadInfo->LoopThreadSmall.web_add,ThreadInfo->LoopThread.web_add, index_nodeweb,ThreadInfo->nodeWQ->num_web_valid,//ThreadInfo->nodeWQ->num_web, //web

			 	//link------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
			 	ThreadInfo->LoopThread.link_okwrited ,ThreadInfo->LoopThread.link_download_ok,ThreadInfo->LoopThread.link_download ,ThreadInfo->LoopThread.link_bad,  //link

			 	//needsleeptime------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
			 	needsleeptime, //needsleeptime

			 	//parse------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
			 	ThreadInfo->LoopThreadSmall.link_parse,ThreadInfo->LoopThread.link_parse_new//,ThreadInfo->LoopThread.link_parse//parse

		 	 );
	}
	return needsleeptime;
}
int ThreadInfo_Free(struct THREADINFO *ThreadInfo)
{

	//释放所有的节点空间

	DeleteQLAll(ThreadInfo->QLWgetWaiting);
	//DeleteQLAll(ThreadInfo->QLWgetWaiting_error);

	//DeleteQLAll(ThreadInfo.QLWgetWorking);
	DeleteQLSHAll( ThreadInfo->QLTaskSH_waiting);
	DeleteQLSHAll( ThreadInfo->QLTaskSH_working);
}
/*
int check_sh_working(struct THREADINFO *ThreadInfo)
{
	struct QNodeThread *thread= ThreadInfo->nodeWQ->QLThread->front;
	while(thread)
	{
		if(thread->Thread->LoopBig.sh_working > 0) return 1;
		thread = thread->next;
	}
	return 0;
}
*/
MYSQL *ConnDatabase(int myid){
	MYSQL *conn;
	while(1){
		conn = mysql_conn_init("manzhua");
		if(!conn) {
			char message[200];
			sprintf(message , "connDatabase  myid=%d  can't open database " , myid);
			write_database_error( conn ,message ,"conn");
			//return 0;
			sleep(1);
			continue;
		}
		return conn;
	}
}


int  DownLoad_new(int myid){
	//思路，每一个下载都是一个任务，不管是WEB还是LINK
	//建立一个任务链表，每个任务有二个状态:1、等待执行 2、下载中。可以对这个任务队列进行删除和添加任务
	//循环链表，处理每个任务的工作情况。
	//原则:1、不能让额度wget限制。2、不能负荷太大
	//这个思路很简洁。

	int tm_last =  time((time_t *) NULL),tm_now;
	char buf[500];
	int needsleeptime=0,index_nodeweb;
	int add_node_type;//添加任务节点类型，0网站，1是链接
	int old_node_num;//节点数量
	int smallloop=0,sleeptime;
	int usertime ;
	//MYSQL *conn= ConnDatabase(myid);
	//conn = mysql_conn_init("manzhua");
	//if(!conn)  { printf ("%d数据库无法打开\n" ,myid);	return 0;}



	struct THREADINFO ThreadInfo;  //这个线程的基本工作信息
	init_ThreadInfo(  myid ,&ThreadInfo,&Num); //初始化线程信息
	make_targetdir_name(&ThreadInfo);
	ThreadInfo.conn = ConnDatabase(myid);
	while( IfOut < 1  ) //循环链表
	{


		 tm_now = time((time_t *) NULL);
		 if( tm_now - tm_last >  7*3600){ //22:26:41  2018-07-31 22:49:34   90
			mysql_close(ThreadInfo.conn);
			sleep(1);
			ThreadInfo.conn= ConnDatabase(myid);
		 	tm_last = tm_now;
		 }

		/*
		sprintf(buf , "SELECT   UNIX_TIMESTAMP(`tm`) ,`mylock`,`layer`,`download`,`loop`,`web_or_link` ,`size_last` FROM  `manzhua`.`link_md5` WHERE `link_md5`.`md5` = CAST( 0xc284595c117cce72011c5d7ab1c7f24e AS BINARY ) LIMIT 1");
		if (mysql_query (ThreadInfo.conn, buf))   printf("error [%s] \n",buf);
		mysql_free_result(mysql_store_result(ThreadInfo.conn));
		 */
		//两个队列，一个是WGET工作队列，一个WGET等待队列
		//每圈初始化一些统计变量
		 init_LoopThreadSmall(&ThreadInfo);
		//开始
		//-----------------------------------------------------------------------
		//一、处理WEGT工作队列，WgetQLWorking，把新任务加入WgetQLWaiting等待队列
		//-----------------------------------------------------------------------
		Do_WgetQLWorking(  &ThreadInfo);


		//-----------------------------------------------------------------------
		//二、取网址。根据等待处理的节点数量，取出网址链接加入等待队列中
		//-----------------------------------------------------------------------

		 //Add_node_task( conn, &ThreadInfo );
		//Add_link_node( conn, &ThreadInfo ,ThreadInfo.QListweball->QLWeb);
		//-----------------------------------------------------------------------
		//三、组织SH队列，根据新弹夹数量从等待队列中提取节点加入弹夹中 ,并运行SH
		//-----------------------------------------------------------------------
		if(    IsWeibo == ThreadInfo.nodeWQ->type
			&& ToolsWget == ThreadInfo.nodeWQ->Tools
			&&  (Connection_pppoe_all == ThreadInfo.nodeWQ->Connection || Connection_pppoe_web == ThreadInfo.nodeWQ->Connection )
		 )
		{
			//微博同时采集20个文件可以，超过马上就封ip。目前的策略是，同时采集20个微博搜索页面，采集完毕后，然后马上换ip。这种方法仅适合专用采集微博服务器。单服务器每日采集量3万以上。
			//用chrome采集特别慢，现在用wget速度快了很多。
			//微博的采集，只需要采集一层，从这层提取所有的微博信息。这点有别于其他采集。
			//后续开发的内容，针对某个关键词页面进行第二页，第三页等多页面的深度采集。
			if( 0 == ThreadInfo.LoopBig.sh_working){
				restartConnection();
				Create_and_run_sh_file( &ThreadInfo);
			}
		}
		else
			Create_and_run_sh_file( &ThreadInfo); //OK

		//Create_and_run_sh_file_error(conn,  &ThreadInfo); //分配错误任务

		//-----------------------------------------------------------------------
		//四、SLEEP AND PRINT INFO
		//-----------------------------------------------------------------------
		//看看两次循环间隔时间如果大于3秒就继续循环，否则休息一会



		//end_check_WgetML =time((time_t *) NULL);
		//if(end_check_WgetML - begin_check_WgetML > MaxCheckLinklistIntervalTime)
		//	needsleeptime = 1   ;
		//else
		//	needsleeptime = MaxCheckLinklistIntervalTime   ;
		//if(smallloop < 1) needsleeptime = 3;
		//else needsleeptime = (int)(ThreadWgetMaxnum / (ThreadInfo.loop_link_download_ok_num+1))-1;
		//显示工作信息
		//if( 2<1 && /*IsWeibo == ThreadInfo.type || IsWeiXin== ThreadInfo.type ||*/ IsSearch==   ThreadInfo.QListweball->type)
		//-----------------------------------------------------------------------
		//四、新文件目录
		//-----------------------------------------------------------------------
		do_targetdir( &ThreadInfo);


		//-----------------------------------------------------------------------
		//五、统计
		//-----------------------------------------------------------------------
		needsleeptime = tongji(&ThreadInfo  );





		//-----------------------------------------------------------------------
		//每个线程没有全部完成一圈采集，不能进入下一圈采集,
		//要有多次扫描机制，第一次扫描网址，可能由于多层网站多，而
		//-----------------------------------------------------------------------
		//if(NULL == ThreadInfo.node_web && ) ThreadInfo.node_web = ThreadInfo.nodeWQ->QLWeb->front;
		if(
			NULL == ThreadInfo.node_web_new
			// && 0 == check_sh_working(&ThreadInfo )
			&&   NULL == ThreadInfo.QLWgetWaiting->front //  0 ==  ThreadInfo.LoopBig.wget_waiting_all //&&
			&&   NULL == ThreadInfo.QLTaskSH_working->front // 0 ==  ThreadInfo.LoopBig.sh_working	//&&
			//&&  0 ==  ThreadInfo.nodeWQ->LoopQueue.wget_waiting_all
			//&&  0 ==  ThreadInfo.nodeWQ->LoopQueue.sh_working
		  ) {
			usertime = time((time_t *) NULL) - ThreadInfo.LoopThread.tm_work_begin ;
			//显示线程自己升级信息
			sprintf(buf,"Thread:%2d %2d/%d  loop usetime=%4d nodeWQ=%d %d doweb=%4d/%d/%d link=%d sleep=%d" ,
				ThreadInfo.myid,ThreadInfo.loop_thread,   ThreadInfo.nodeWQ->loop_WQ,
				//nodeWQ
				usertime,
				ThreadInfo.nodeWQ->index,
				ThreadInfo.nodeWQ->type,
				//web
				ThreadInfo.LoopThread.web_add,ThreadInfo.nodeWQ->num_web_valid,ThreadInfo.nodeWQ->num_web,
				ThreadInfo.LoopThread.link_parse_new,
				ThreadInfo.nodeWQ->IntervalTimeWeb -usertime
				);

			Recordwork(buf,Recordworkfile);
			printf("%s\n",buf);

			//检查是否整个队列采集完一圈
			//if(ThreadInfo.loop_thread == ThreadInfo.nodeWQ->loop_WQ )

			pthread_mutex_lock(&mymutex_check_web_loop);
			check_web_loop( &ThreadInfo );
			pthread_mutex_unlock(&mymutex_check_web_loop);

			if(usertime < ThreadInfo.nodeWQ->IntervalTimeWeb  )   sleep(ThreadInfo.nodeWQ->IntervalTimeWeb -usertime); //&&  NULL == ThreadInfo.QLWgetWaiting->front && NULL == ThreadInfo.QLTaskSH_working->front
			init_LoopThread(&ThreadInfo );

		}


		//-----------------------------------------------------------------------
		//休息
		//-----------------------------------------------------------------------
		//if(needsleeptime > 0 )  sleep(needsleeptime);
		//if(ThreadInfo.LoopBig.sh_working == 0 )
		//	sleep(10);
		//else
		if(needsleeptime <  0)
			sleep(1);
		else
			sleep(2);
		smallloop++;
	}

	ThreadInfo_Free(&ThreadInfo);
	mysql_close(ThreadInfo.conn);

	sprintf(buf,"%2d  i out......................................Download_new"   ,myid);
	printf("%s\n"   ,buf);
	Recordwork(buf,Recordworkfile);

	return 0;
}
//-------------------------------------------------------------------------------------------------------------------------------------------------
int ProxyWebNum=0;
char ProxyWeb[2][200];
int QLProxyNodeNum = 50;
/*
int ProxyGetWeb()
{
	ProxyWebNum=0;
	int len,n;
	char proxywebfile[100],proxyweb[1024],proxyfile[200];
	FILE * FILE_proxy_file;
	sprintf(proxywebfile,"%s/proxyweb.cfg",NowWorkingDir);
	sprintf(proxyfile,"%s/proxyfile" ,NowWorkingDir );
	FILE_proxy_file=fopen(proxywebfile,"r");
	if (FILE_proxy_file == NULL) perror ("Error opening file");
	else
	{
		while ( ! feof (FILE_proxy_file) )
		{
			if ( fgets (proxyweb  , 1024 , FILE_proxy_file) != NULL )
			{
				//110.190.96.249:18186
				len  = strlen(proxyweb);
				//删除回车等标记
				n =1;
				while(1)
				{
					if(isspace(proxyweb[len-n]) ) proxyweb[len-n] = '\0';
					else break;
					n++;
				}
				sprintf(ProxyWeb[ProxyWebNum] , "wget -q  \"%s%d\"  -O %s" ,proxyweb,QLProxyNodeNum,proxyfile );
				printf("ProxyWebNum=%d  [%s]\n",ProxyWebNum,ProxyWeb[ProxyWebNum] );
				ProxyWebNum++;

			}
		}
		fclose (FILE_proxy_file);

	}

}
*/
int MytimeNew(time_t the_time ,char *nowtime_str)
{
 	//给定时间戳，返回格式时间

      char buf[200];
	struct tm *tm_ptr;
	//time_t the_time;
	//(void) time(&the_time);
	tm_ptr=localtime(&the_time);
	sprintf(buf,"%02d-%02d-%02d %02d:%02d:%02d",(tm_ptr->tm_year+1900),tm_ptr->tm_mon+1,tm_ptr->tm_mday, tm_ptr->tm_hour,tm_ptr->tm_min,tm_ptr->tm_sec);
	strcpy(nowtime_str, buf);

}

 int timestr2filename(char *nowtime_str)
{
	char *p;
	ReplaceStr(nowtime_str," ","_");
	p = rindex(nowtime_str,':');
	*p = '\0';
}


int get_timestr_not_s(int tm , char *timestr)
{
	//给时间戳返回不带秒的时间字符串,用于文件存储

	MytimeNew(tm ,timestr);
	timestr2filename(timestr);
	// "2016-12-12 11:21:12" => "2016-12-12 11:21:00"
	/*
	int len;
	len = strlen(timestr);
	timestr[len-1] = '0';
	timestr[len-2] = '0';
	*/

}
int readproxy2QL( int tm,int numgoodproxy  )
{
	int num = 0;
	char remote_name[200],proxyfile[200],timestr[50] ;
	//远程文件路径名
	//MytimeNew(tm ,timestr);
	//timestr2filename(timestr);
	get_timestr_not_s(tm ,timestr);
	sprintf(remote_name ,"proxy/%s" ,timestr);
	//本地文件路径名
	sprintf(proxyfile,"%s/%s",NowWorkingDir,remote_name);

	if(1== download_a_file(remote_name,1 )   ) {
		char proxy[1025];
		FILE * FILE_proxy_file;
		FILE_proxy_file=fopen(proxyfile,"r");
		if (FILE_proxy_file == NULL)
			perror ("Error opening file");
		else{
			while ( ! feof (FILE_proxy_file) ){
				if ( fgets (proxy  , 1024 , FILE_proxy_file) != NULL ){
					//删除回车等标记
					//110.190.96.249:18186
					Del_other(proxy);
					if(checkproxy(proxy) >0){
						InsertQLProxy( QLProxy,proxy,numgoodproxy,Num.proxy);
						num++;
						Num.proxy++;
						//printf("addnum=%d [%s]\n",addnum,ProxyWeb[i]);
					}
				}
			}
			fclose (FILE_proxy_file);
		}
	}
	return num;
}
int cmp_tm_not_s(int tm1,int tm2)
{
	//比较2个时间戳，是否未同一分钟，是返回1，不是返回0
	char timestr1[50] ,timestr2[50];
	get_timestr_not_s( tm1 , timestr1);
	get_timestr_not_s( tm2 , timestr2);
	if( 0 == strcmp(timestr1,timestr2))
		return 1;
	else
		return 0;

}
int ProxyGet(int myid, QListProxy *QLProxy, int numgoodproxy,int ThreadWgetMaxnum )
{
	int lastoknum = 0;
	char buf[100];
	sprintf(buf,"myid=%d ProxyGet numgoodproxy=%d---weibo=%d weibo_search=%d weixin=%d search=%d  ",myid, numgoodproxy ,Num.thread_weibo, Num.thread_weibo_search,Num.thread_weixin,Num.thread_search);
	printf("%s\n"   ,buf);
	Recordwork(buf,Recordworkfile);

	if(numgoodproxy >0 )
	{
			struct PROXYTOTAL proxy_total;
			//ProxyGetWeb();
			//注意地理API经常换链接，要测试
			int  tm_now,tm_last;
			int loop=0 ;

			tm_last =time((time_t *) NULL) -60*5;//向1分钟

			while(IfOut<1)
			{
				//提取proxy
				proxy_total.add= 0;
				if(CountQLProxyOK(QLProxy,numgoodproxy)< ThreadWgetMaxnum*2){

						//从上次提取时间到现在时间之间的文件都加入队列，避免遗漏
						tm_now = time((time_t *) NULL);
						while(IfOut<1 && 0 == cmp_tm_not_s (tm_now ,tm_last) ){
								proxy_total.add = proxy_total.add  +  readproxy2QL( tm_last , numgoodproxy );
								tm_last = tm_last + 60; //向后推1分钟
						}
						//tm_last = tm_now;
				}

				//清理proxy
				proxy_total.free=CountQLProxyOK(QLProxy, numgoodproxy);
				ClearQLProxy(QLProxy,numgoodproxy ,&proxy_total) ;
				printf("myid=%d proxy  loop=%d  add/clear =%d/%d    num: free=%d  alive=%d  indexall=%d  goodproxy=%d sleep=15\n" ,myid,loop,proxy_total.add,proxy_total.clear, proxy_total.free,proxy_total.alive,Num.proxy,Num.goodproxy);
				loop++;

				sleep(15);
			}
			//把好代理写个文件
			lastoknum = WriteQLProxyFile(QLProxy,numgoodproxy);

	}
	sprintf(buf,"%2d  i out....................ProxyGet......lastoknum=%d.........."   ,myid,lastoknum);
	printf("%s\n"   ,buf);
	Recordwork(buf,Recordworkfile);

	return 0;
}


 /************************* this is the thread code ***************************/
 void *Dataaa(void * arg)   //(void * arg)
 {


	int myid=*(int *) arg;

	printf("myid=%d\n",myid);

	if(0== myid   )
	{
		FirstWork(myid); //零号线程安排为调度线程AfterWork
	}
	else if(THREADINFO_Proxy_No  == myid  )
	{

		ProxyGet(myid ,QLProxy,Num.goodproxy,25); //代理服务器处理线程
	}
	else
	{
	 	 DownLoad_new(myid);
	}

	return arg;
 }




int Create_thread(struct MYNUM *Num)
{//创建32个DATAAA线程，开始工作

	   int worker;
	   pthread_t threads[Num->thread_all];                /* holds thread info */
	   int ids[Num->thread_all];                          /* holds thread args */
	   int errcode;                                /* holds pthread error code */
	   int *status;                                /* holds return code */


	   /* create the threads */
	   for (worker=0; worker<Num->thread_all; worker++) {
		     ids[worker]=worker;
		    // printf("ids[%d]=%d\n",worker,ids[worker]);
		     // sleep(1);
		     if (errcode=pthread_create(&threads[worker],/* thread struct             */
		 		       NULL,                    /* default thread attributes */
		 		       Dataaa,                    /* start routine             */
		 		     &ids[worker])) {       /* arg to routine      &ids[worker])) {         */
		      errexit(errcode,"pthread_create");
		    }
			  sleep(1);
	   }

	   /* reap the threads as they exit */
	   for (worker=0; worker<Num->thread_all; worker++) {
	     /* wait for thread to terminate */
	     if (errcode=pthread_join(threads[worker],(void *) &status)) {
	     	//printf("ids[worker]=%d,worker=%d\n",ids[worker],worker);
	      errexit(errcode,"pthread_join");
	    }


	     /* check thread's exit status and release its resources */
	     if (*status != ids[worker]) {
	       fprintf(stderr,"thread %d terminated abnormally\n",worker);
	       exit(1);
	    }

	   }
	   return(0);

}



int clear_manzhu_database()
{
	//清理表，把所有的锁都打开
	printf("二、clear_manzhu_database -----------------------------------------------\n");
  	MYSQL *conn;
	conn = mysql_conn_init("manzhua");
	char sql[512],buf[512];

	// "set interactive_timeout=24*3600";



	//清理超过5天未访问的链接
	unsigned int tm ,tmp ,endtm;
	tm=time((time_t *) NULL);
	tmp = tm - CaiJiClearTime;

	//删除link_md5表多余数据
	sprintf(sql, "DELETE FROM `manzhua`.`link_md5` WHERE UNIX_TIMESTAMP(`link_md5`.`tm`) < %d" ,tmp);
	printf("1  %s.............\n" , sql);
	if (mysql_query (conn, sql))   printf("link_md5 clear_manzhu_database error \n");
	//只要是sql语句就要释放，不管有没有返回结果******************************************************8
	//else mysql_free_result(mysql_store_result(conn));

	//链接降圈
	sprintf(sql , "UPDATE `manzhua`.`link_md5` SET  `loop`='1'  WHERE  `loop`>1" );
	printf("2  %s.............\n" , sql);
	if (mysql_query (conn, sql))   printf("error [%s] \n",sql);
	//else mysql_free_result(mysql_store_result(conn));

	//link_md5链接库解锁
	//web_or_link要置IsLink，如果原来的网址删除了，这个练级在算法里就无法采集了。
	sprintf(sql, "UPDATE `manzhua`.`link_md5` SET  `mylock` = '0' ,`tm` = FROM_UNIXTIME(UNIX_TIMESTAMP(`tm`) -301)  ,`web_or_link`='%d'  WHERE  1" ,IsLink);//`tm`= '0000-00-00 00:00:00',置0没关系，Firstwork中有保护，到2点小于20小时刚启动的程序，不程序不重新启动
	printf("3  %s.............\n" , sql);
	if (mysql_query (conn, sql))   printf("error [%s] \n",sql);
	//else mysql_free_result(mysql_store_result(conn));

	//优化
	sprintf(sql, "OPTIMIZE TABLE  `manzhua`.`link_md5`");
	printf("4  %s.............\n" , sql);
	if (mysql_query (conn, sql))   printf("error [%s] \n",sql);
	else mysql_free_result(mysql_store_result(conn)); //这个地方好像必须要加




	//删除web_md5_no
	sprintf(sql, "DELETE FROM `manzhua`.`web_md5_no` WHERE 1" );
	printf("5  %s.............\n" , sql);
	if (mysql_query (conn, sql)) {
		//2014 Commands out of sync; you can't run this command now    https://blog.csdn.net/luketty/article/details/5745000   =>mysql_free_result(mysql_store_result(conn));
		int errno =  mysql_errno (conn);
		printf("error %d  %s:\n%s\n\n" ,errno ,sql, mysql_error(conn));
		//sleep(10000);
	}
	//else mysql_free_result(mysql_store_result(conn));



	mysql_close(conn);
	return 0;
}

int
create_manzhu_database(){
	char sql[2000],buf[100];

	MYSQL *conn;
	conn = mysql_conn_init(NULL);

	if(!conn)
	{
		//printf ("数据库无法打开\n" );
		RecordMessage("数据库无法打开" ,Recordworkfile,1);
		return 0;
	}
	mysql_query(conn,"set wait_timeout = 24*3600");
	//mysql_free_result(mysql_store_result(conn));

	mysql_query(conn, "set interactive_timeout=24*3600");
	//mysql_free_result(mysql_store_result(conn));

	sprintf(sql ,"DROP DATABASE `manzhua` ");
	if (mysql_query (conn, sql))
		RecordMessage(sql ,Recordworkfile,1);
	//else		mysql_free_result(mysql_store_result(conn));


	sprintf(sql , "CREATE DATABASE `manzhua` DEFAULT CHARACTER SET gbk COLLATE gbk_chinese_ci");
	if (mysql_query (conn, sql))
		RecordMessage(sql ,Recordworkfile,1);
	//else		mysql_free_result(mysql_store_result(conn));


	//link_md5
	printf("Myip=%s",Myip);sleep(5);
	if(strstr(Myip,"192.187.111.146"))
		sprintf(buf,"MyISAM");
	else{
		sprintf(buf,"MEMORY");
		sprintf(sql , "SET max_heap_table_size = 4048576000"); //4G
		if (mysql_query (conn, sql)) RecordMessage(sql ,Recordworkfile,1);
		//mysql_free_result(mysql_store_result(conn));

	}
	sprintf(sql ,"CREATE TABLE IF NOT EXISTS `manzhua`.`link_md5` (  `md5` binary(16) NOT NULL COMMENT '链接的md5码',  `tm` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP ,  `mylock` tinyint(3) unsigned NOT NULL DEFAULT '0' ,`layer` tinyint(4) NOT NULL DEFAULT '-1', `loop` SMALLINT( 5 ) UNSIGNED NOT NULL DEFAULT  '0',`download` tinyint(4) NOT NULL DEFAULT '%d',`web_or_link` tinyint(3) unsigned NOT NULL DEFAULT '100',`size_last` MEDIUMINT NOT NULL DEFAULT  '0' COMMENT  '大小', PRIMARY KEY (`md5`)) ENGINE=%s DEFAULT CHARSET=latin1",Download_OKInit,buf);
	if (mysql_query (conn, sql))
		RecordMessage(sql ,Recordworkfile,1);
	//else		mysql_free_result(mysql_store_result(conn));


	//web_md5_no
	 sprintf(sql , "SET max_heap_table_size = 104857600");// 100M
	if (mysql_query (conn, sql))
		RecordMessage(sql ,Recordworkfile,1);
	//else		mysql_free_result(mysql_store_result(conn));

	//twoleveldomain 存储二级域名的开始部分，news.sian.com.cn => new. 多个news.sian.com.cn ，beijing.sian.com.cn =>news.beijing.  用于屏蔽域名的查询，可减少一次查询次数
	sprintf(sql ,"CREATE TABLE IF NOT EXISTS `manzhua`.`web_md5_no` (    `md5` binary(16) NOT NULL,  `index` smallint(6) NOT NULL DEFAULT '-1',PRIMARY KEY (`md5`))  ENGINE=MEMORY DEFAULT CHARSET=gbk");//MyISAM  InnoDB
	if (mysql_query (conn, sql))
		RecordMessage(sql ,Recordworkfile,1);
	//else		mysql_free_result(mysql_store_result(conn));


	//analysis
	sprintf(sql , "CREATE DATABASE IF NOT EXISTS `analysis` DEFAULT CHARACTER SET gbk COLLATE gbk_chinese_ci");
	if (mysql_query (conn, sql))
		RecordMessage(sql ,Recordworkfile,1);
	//else		mysql_free_result(mysql_store_result(conn));

	//创建链接格式数据表，用于判断是文章链接，还是频道链接，文章链接就采集多层。减少多层链接采集是提高采集效率的有效方法
	sprintf(sql ,"CREATE TABLE IF NOT EXISTS `analysis`.`link_format` ( `md5` binary(16) NOT NULL,  `num` tinyint(3)  unsigned NOT NULL DEFAULT '1', `format` varchar(255) NOT NULL,  PRIMARY KEY (`md5`)) ENGINE=MyISAM DEFAULT CHARSET=gbk");
	if (mysql_query (conn, sql))
		RecordMessage(sql ,Recordworkfile,1);
	//else		mysql_free_result(mysql_store_result(conn));


	mysql_close(conn);
	RecordMessage("create database" ,Recordworkfile,1);
	return 1;


	/*
	//set global innodb_buffer_pool_size = 1400000000;
	//SELECT COUNT(@@GLOBAL.innodb_buffer_pool_size)  //查看innodb_buffer_pool_size
	innodb_buffer_pool_size - 这对Innodb表来说非常重要。Innodb相比MyISAM表对缓冲更为敏感。MyISAM可以在默认的 key_buffer_size 设置下运行的可以，然而Innodb在默认的 innodb_buffer_pool_size 设置下却跟蜗牛似的。由于Innodb把数据和索引都缓存起来，无需留给操作系统太多的内存，因此如果只需要用Innodb的话则可以设置它高达 70-80% 的可用内存。一些应用于 key_buffer 的规则有 -- 如果你的数据量不大，并且不会暴增，那么无需把
	innodb_additional_pool_size - 这个选项对性能影响并不太多，至少在有差不多足够内存可分配的操作系统上是这样。不过如果你仍然想设置为 20MB(或者更大)，因此就需要看一下Innodb其他需要分配的内存有多少。
	innodb_log_file_size 在高写入负载尤其是大数据集的情况下很重要。这个值越大则性能相对越高，但是要注意到可能会增加恢复时间。我经常设置为 64-512MB，跟据服务器大小而异。
	innodb_log_buffer_size 默认的设置在中等强度写入负载以及较短事务的情况下，服务器性能还可 以。如果存在更新操作峰值或者负载较大，就应该考虑加大它的值了。如果它的值设置太高了，可能会浪费内存 -- 它每秒都会刷新一次，因此无需设置超过1秒所需的内存空间。通常 8-16MB 就足够了。越小的系统它的值越小。
	innodb_flush_logs_at_trx_commit 是否为Innodb比MyISAM慢1000倍而头大？看来也许你忘了修改这个参数了。默认值是 1，这意味着每次提交的更新事务（或者每个事务之外的语句）都会刷新到磁盘中，而这相当耗费资源，尤其是没有电池备用缓存时。很多应用程序，尤其是从 MyISAM转变过来的那些，把它的值设置为 2 就可以了，也就是不把日志刷新到磁盘上，而只刷新到操作系统的缓存上。日志仍然会每秒刷新到磁盘中去，因此通常不会丢失每秒1-2次更新的消耗。如果设置 为 0 就快很多了，不过也相对不安全了 -- MySQL服务器崩溃时就会丢失一些事务。设置为 2 指挥丢失刷新到操作系统缓存的那部分事务。

	*/



}
#define DEV0 "eth0"
#define DEV1 "eth1"
/*获得本地机器某网卡网卡名为eth_name的IP*/
/*如果参数为NULL, 则默认为eth0*/
const char *
get_local_ip(const char* eth_name)
{
    int sock;
    struct sockaddr_in sin;
    struct ifreq ifr;

    if(NULL == eth_name)
		eth_name = "eth0";

    sock = socket(AF_INET, SOCK_DGRAM, 0);
                           /*建立socket*/
    if (sock == -1)
      {
         perror("socket");
         return (char*)NULL;
      }

    strncpy(ifr.ifr_name, eth_name, IFNAMSIZ);
    ifr.ifr_name[IFNAMSIZ - 1] = 0;

    if (ioctl(sock, SIOCGIFADDR, &ifr) < 0)
      {
        perror("ioctl");
		close (sock);
        return (char*)NULL;
      }

    memcpy(&sin, &ifr.ifr_addr, sizeof(sin));
    //fprintf(stdout, "eth0: %s\n", inet_ntoa(sin.sin_addr));
    close (sock);

    return inet_ntoa(sin.sin_addr);
}
int mymkdir_system(char *dir)
{
	  if((access(dir,F_OK))!=-1)
	    {
	       return 0;
	    }
	    else
	    {
	    	char buf[100];
		sprintf(buf,"mkdir %s",dir);
		system(buf);
		return 1;
	    }

}

int InitMy(struct MYNUM *Num)
{
		int i;
		 Num->proxy = 0;
		printf("-------------------InitMy begin   Num->wget=%d\n", Num->wget);

		if(0 == LimitRate  )
			onewgetLimitRate = 0;
		else
			onewgetLimitRate = (int)((LimitRate/8)/   Num->wget  ) ;
		printf("onewgetLimitRate=%d k    \n",onewgetLimitRate);

}
int Init_Num(struct MYNUM *Num)
{
		Num->thread_all = 0;
		Num->thread_web = 0;//网页下载数量
		Num->thread_weibo = 0;//主微博采集线程数量
		Num->thread_weixin = 0;//微信采集线程数量
	 	Num->thread_search = 0;//采集搜索引擎的线程数量
	 	Num->thread_weibo_search = 0;//微博搜索的数量
	 	Num->thread_download_index = 0;

		Num->FirstWork = 0;
		Num->goodproxy = 0;//队列使用代理的数量
		Num->proxy = 0;//总计代理服务器下载数量
		Num->WebQueue = 0; //采集队列的数量


		Num->wget = 0;//同时工作的wget 个数

}

int count_nodeWQ(QNodeWebQueue* nodeWQ ,int type)
{
	int num=0;
	QNodeWeb *p=nodeWQ->QLWeb->front;
	while(p)
	{
		if(p->layer == type || 0 == type)
			num++;
		p= p->next;
	}
	return num;
}
int display_QListWebQueue_info(struct QListWebQueue *QLWebAll)
{
		printf("---------------display_QListWebQueue_info---------------------------\n");

		char buf[200];
		QNodeWebQueue* nodeWQ;
		nodeWQ = QLWebAll->front;
		while(nodeWQ  )
		{
			sprintf(buf,"./error/%s",nodeWQ->web);
			mkdir(buf,0755);
			sprintf(buf,"%2d-----type=%8s----web=[%20s]---(%d/%d/%d/%d)---num_thread=%2d  index_proxy=%2d/%d", nodeWQ->index,typestr[nodeWQ->type],nodeWQ->web,
				count_nodeWQ(nodeWQ,1) ,count_nodeWQ(nodeWQ,2) ,count_nodeWQ(nodeWQ,3) ,count_nodeWQ(nodeWQ,0) ,
				nodeWQ->num_thread , nodeWQ->index_proxy,Num.goodproxy);
			Recordwork(buf,Recordworkfile);
			printf("%s\n" ,buf);
			nodeWQ = nodeWQ->next;

		}
		sleep(3);
		printf("------------------------------------------------------------------\n");
		return 0;
}
int InitQLmain()
{
		//QLProxy
		QLProxy =(QListProxy*)malloc(sizeof(QListProxy));
		if(QLProxy)
		{
			InitQLProxy(QLProxy);
			RecordMessage("InitQLProxy work ok" ,Recordworkfile,1);
		}
		else
		{
			RecordMessage("InitQLProxy work error" ,Recordworkfile,1);
			return 0;
		}

		QLProxyBad=(QListProxy*)malloc(sizeof(QListProxy));
		if(QLProxyBad)
		{
			InitQLProxy(QLProxyBad);
			RecordMessage("InitQLProxy work ok" ,Recordworkfile,1);
		}
		else
		{
			RecordMessage("InitQLProxy work error" ,Recordworkfile,1);
			return 0;
		}
		//QLWebAll
		QLWebAll =(QListWebQueue*)malloc(sizeof(QListWebQueue));
		if(QLWebAll)
		{
			InitQLWebQueue(QLWebAll);
			//system("ps -e -o 'comm,rsz' | grep estar_manzhua >>memory.txt ");
			RecordMessage("InitQLWebQueue work ok" ,Recordworkfile,1);
		}
		else
		{
			RecordMessage("InitQLWebQueue work error" ,Recordworkfile,1);
			return 0;
		}

		//QLShieldWeb
		QLShieldWeb=(QListShieldWeb*)malloc(sizeof(QListShieldWeb));
		if(QLShieldWeb)
		{
			InitQLShieldWeb(QLShieldWeb);
			RecordMessage("InitQLShieldWeb work ok" ,Recordworkfile,1);
		}
		else
		{
			RecordMessage("InitQLShieldWeb work error" ,Recordworkfile,1);
			return 0;
		}


		return 1;

}
int main()
{
	RecordMessage("\n\n\n\n\n\n\n\n\n\n\n\n\n\n" ,Recordworkfile,1);
	//以队列为核心
	char buf[500];
	int i;
	//设置字符环境
	sprintf(buf,"LANG=\"en_US:en\"");
	system(buf);
	//获取IP地址
	//get_ip(Myip);
	Myip[0] = '\0';
	//printf("Myip--%s\n",Myip);
	//Myip[0] = '\0';
	/*
	static const  char *myip = NULL; //存储本机的IP地址
  	myip = get_local_ip(DEV0);
	if(myip == NULL) myip = get_local_ip(DEV1);
	sprintf(Myip,"%s" ,myip);
	*/
	//printf("Myip--%s\n",Myip);

	 mymkdir_system("/estar");


	//创建数据库
	create_manzhu_database();

	unlink(testfile);
	unlink("memory.txt");
	BigLoop = 1;
	//大循环开始，每次循环24小时，更新网址链接、微博关键词、频繁采集关键词
	while(1)
	{
		//写工作记录
		if(1 == BigLoop)
		{
			//RecordMessage("\n\n\n\n\n\n\n\n\n\n\n\n\n\n" ,Recordworkfile,1);
		}

		//初始化统计
		Init_Num(&Num);
		//system("echo \"\n\nbegin\" >>memory.txt ");
		//system("ps -e -o 'comm,rsz' | grep estar_manzhua >>memory.txt ");

		//初始化队列
		if(0 == InitQLmain() ) break;

	     //清理数据库
		clear_manzhu_database();
		//system("ps -e -o 'comm,rsz' | grep estar_manzhua >>memory.txt ");
		RecordMessage("clear_manzhu_database work end" ,Recordworkfile,1);



		//读配置文件信息到公共变量中
		if(ReadcfgNew(QLWebAll,&Num) == 0)//;//&File ,
	 	{
			RecordMessage("ReadcfgNew is error is 0" ,Recordworkfile,1);
			break;
		}
		else
		{
			RecordMessage("ReadcfgNew is ok" ,Recordworkfile,1);
		}
		//system("ps -e -o 'comm,rsz' | grep estar_manzhua >>memory.txt ");
		IfOut = 0;

		//显示线程信息
		//printf("sleep InitMy\n");
		InitMy(&Num);

		//DownloadTools_Read();



		sleep(1);



		//读网址信息


		RecordMessage("------------------------------------------------------------" ,Recordworkfile,1);
		sprintf(buf,"--BigLoop=%d----IP=%s- -%dk-- ",BigLoop ,Myip,onewgetLimitRate);
		RecordMessage(buf,Recordworkfile,1);
		sprintf(buf,"--Num_Thread=%d-- web=%d  weibo=%d weibo_search=%d weixin=%d search=%d control=1 proxy=1 Num.goodproxy=%d", Num.thread_all,Num.thread_web, Num.thread_weibo, Num.thread_weibo_search,Num.thread_weixin,Num.thread_search,Num.goodproxy);
		RecordMessage(buf,Recordworkfile,1);
		sprintf(buf,"--QLnum=%d ----", Num.WebQueue);
		RecordMessage(buf,Recordworkfile,1);

		//display_QListWebQueue_info(QLWebAll);

		RecordMessage("------------------------------------------------------------" ,Recordworkfile,1);
		//printf("QLShieldWeb num =%d\n" ,QLShield_Domains_Count(QLShieldWeb) );
		QLShield_Domains_Count(QLShieldWeb);
		sleep(3);
		//开始采集
		Create_thread(&Num);

		//多线程结束显示
		RecordMessage("run over",Recordworkfile,1);
		BigLoop++;

		//system("ps -e -o 'comm,rsz' | grep estar_manzhua >>memory.txt ");

		DeleteQLProxy( QLProxy );
		DeleteQLProxy( QLProxyBad);
		DeleteQLWebQueue(QLWebAll);
		DeleteQListShieldWebAll(QLShieldWeb);
		DownloadTools_Free();
		//system("ps -e -o 'comm,rsz' | grep estar_manzhua >>memory.txt ");

		RecordMessage("free DeleteQLProxy  DeleteQLWebQueue  DeleteQListShieldWebAll",Recordworkfile,1);

		//free_str_arr(&KwDeleteHtml);
		//free_str_arr(&UrlPingBiInEnd);
		//free_str_arr(&UrlPingBiInPublic);

		RecordMessage("sleep all " ,Recordworkfile,1);


		sleep(10);

	}
	//DeleteQLProxyAll(QLProxy);

	return 0;
}


