// PMP报名流程

/*
    登录地址： http://exam.chinapmp.cn/login.shtml
    用户中心： http://user.chinapmp.cn/index.shtml
    开始报名： http://user.chinapmp.cn/examsign.shtml
    个人信息确认： http://user.chinapmp.cn/examsign;info.shtml
    选择考点： http://user.chinapmp.cn/examsign;sign.shtml
    查看报名后是否成功页面： http://user.chinapmp.cn/myexam.shtml
*/


// ===============================
// part1 登录
// 打开调试台win:ctrl+shift+i  mac:command+shift+i, 切换到NetWork标签,之后按esc键呼出Console
// 打开下面网址
// http://exam.chinapmp.cn/login.shtml
// 当页面停止网络请求后, 无论页面显示什么内容, 将以下代码复制到Console中并回车执行
// 直至出现登录完成弹窗
// 注意:tryLogin方法填写自己的中文账号密码
// ===============================

function appScripts(cb) {
    let _src = scriptArr.shift();
    if (_src) {
        let s = document.createElement('script');
        s.onload = () => {
            console.log(`add script done ==> ${_src}`);
            appScripts(cb);
        };
        s.src = _src;
        document.body.appendChild(s);
    } else {
        cb();
    }
}

function tryLogin(uName, uPass) {
    SHOW.Ajax.Exam.Login.Save(0, uName, uPass, res => {
        if (!res.error) {
            console.log(res);
            alert('登录成功, 进入下一步');
            window.location.href = 'http://user.chinapmp.cn/examsign;info.shtml';
        } else {
            console.log(`登录失败, 再次尝试 AT::${Date.now()}`);
            tryLogin(uName, uPass);
        }
    });
}

let scriptArr = [
    'http://card.mugeda.com/js/other/jquery.js',
    'http://card.mugeda.com/js/other/jcomm.js',
    'http://card.mugeda.com/js/other/4BD0ABA8E39F14797B0A73A80C2F1DBE.js',
    'http://card.mugeda.com/js/other/SHOW.Ajax.Exam.Login.js'
];

appScripts(() => {
    tryLogin('王骁121416', '18612964129');
});





// ===============================
// part2.1 承诺书页面
// 检查浏览器地址是否已经跳转至以下地址
// http://user.chinapmp.cn/examsign;info.shtml
// 当页面停止网络请求后, 查看是否显示承诺书页面, 如果不显示则刷新
// 如果显示承诺书页面, 复制下面内容至Console,并回车执行
// 出现'全部注入完成'后, 此时大概率按钮开始60s倒计时,等待倒计时结束后点击按钮进入个人信息确认页
// 正常点击按钮提交个人信息, 如果这个步骤正常, 直接进入part3
// 如果此步骤不正常, 则进入后续流程 part2.2
// ===============================

function appScripts(cb) {
    let _src = scriptArr.shift();
    if (_src) {
        let s = document.createElement('script');
        s.onload = () => {
            console.log(`add script done ==> ${_src}`);
            appScripts(cb);
        };
        s.src = _src;
        document.body.appendChild(s);
    } else {
        cb();
    }
}

let scriptArr = [
    'http://card.mugeda.com/js/other/jquery.js',
    'http://card.mugeda.com/js/other/juimin.js',
    'http://card.mugeda.com/js/other/jcomm.js',
    'http://card.mugeda.com/js/other/A3AE44721F716A2CD79FBF70BDFE01FC.js',
    'http://card.mugeda.com/js/other/examsign.js',
    'http://card.mugeda.com/js/other/jvalidation.js',
    'http://oss.aiyawoc.com/js/pmp/EXAM20210413.js', //考试信息
    'http://card.mugeda.com/js/other/SHOW.Ajax.User.Examsign.info.js'
];

appScripts(() => {
    console.log('全部注入完成');
});


// ===============================
// part2.2 确认防疫承诺书
// 复制以下内容到Console中并回车执行
// 持续等待, 直至跳出弹窗显示'同意完成, 进入下一步'
// 关闭弹窗, 进入part2.3
// ===============================

// SHOW.Ajax.User.Examsign.Agree(EXAM.Id);

function tryAgree() {
    let Ed = '10000044';
    SHOW.Ajax.User.Examsign.Agree(Ed, res => {
        if (res.value) {
            alert('同意完成, 进入下一步');

        } else {
            console.log(`同意失败, 再次尝试AT::${Date.now()}`);
            tryAgree();
        }
    });
}

tryAgree();

// ===============================
// part2.3 确认个人信息
// 修改以下信息为自己的资料
// 修改完成后, 将下列信息复制到Console中并回车
// 等待, 直至出现弹窗显示'保存信息成功, 进入下一步'
// 关闭弹窗, 自动跳转至报名页面
// ===============================

let curUserInfo = {
    Tname: '王骁',
    Gender: '男(Male)',
    Birthday: '/Date(634800141000+0800)/',
    IDtype: '身份证(ID Card)',
    IDnumber: '110108199002121416',
    Graduated: '北京外国语大学',
    Graduation: '/Date(1372656141000+0800)/', //毕业日期
    Major: '其他',
    Edu: '本科(Bacholar)', //学位
    Industry: '信息传输、计算机服务和软件', //行业
    Workunits: '北京铱星在线',
    Workunitstype: '民企', //公司类型
    Position: '项目经理', //职位
    Tel: '02228383259',
    Mobile: '18612964129',
    Email: 'hwtony@live.com',
    Amail: 'liwen@aura.cn',
    Address: '中国 北京市 昌平区 龙跃街',
    Zip: '102208'
}

function trySaveInfo(u) {
    SHOW.Ajax.User.Examsign.SaveInfo(
        u.Tname,
        u.Gender,
        u.Birthday,
        u.IDtype,
        u.IDnumber,
        u.Graduated,
        u.Graduation,
        u.Major,
        u.Edu,
        u.Industry,
        u.Workunits,
        u.Workunitstype,
        u.Position,
        u.Tel,
        u.Mobile,
        u.Email,
        u.Amail,
        u.Address,
        u.Zip,
        res => {
            console.log(res);
            if (res.value) {
                alert('保存信息成功, 进入下一步');
                window.location.href = SHOW.Config.PName + ";sign" + SHOW.Config.Ext;
            } else {
                console.log(`保存信息失败, 再次尝试AT${Date.now()}`);
                trySaveInfo(u);
            }
        });
}

trySaveInfo(curUserInfo);


// ===============================
// part3.1 报名-信息注入
// 检查浏览器地址是否已经跳转至以下地址
// http://user.chinapmp.cn/examsign;sign.shtml
// 当页面停止网络请求后, 无论页面显示什么内容, 将以下代码复制到Console中并回车执行
// 出现'全部注入完成'后, 进入步骤3.2
// ===============================

function appScripts(cb) {
    let _src = scriptArr.shift();
    if (_src) {
        let s = document.createElement('script');
        s.onload = () => {
            console.log(`add script done ==> ${_src}`);
            appScripts(cb);
        };
        s.src = _src;
        document.body.appendChild(s);
    } else {
        cb();
    }
}

let scriptArr = [
    'http://card.mugeda.com/js/other/jquery.js',
    'http://card.mugeda.com/js/other/juimin.js',
    'http://card.mugeda.com/js/other/jcomm.js',
    'http://card.mugeda.com/js/other/61026A313A3252DDCCB247023B60CDAF.js',
    'http://card.mugeda.com/js/other/examsign.js',
    'http://card.mugeda.com/js/other/jvalidation.js',
    'http://oss.aiyawoc.com/js/pmp/EXAM20210413.js', //考试信息
    'http://card.mugeda.com/js/other/SHOW.Ajax.User.Examsign.sign.js'
];

appScripts(() => {
    console.log('全部注入完成');
});

// ===============================
// part3.2 报名
// 修改signInfo中的信息为自己的资料
// 将下列信息复制到Console中并回车执行
// 等待, 直至出现弹窗
// ===============================

// SHOW.Ajax.User.Examsign.Sign();

var signInfo = {
    Ed: '10000044',
    Etitle: ' 2021年6月20日项目管理资格认证考试',
    Stype: '101',
    StypeName: '项目管理师(PMP®)',
    Xing: 'Wang', //你的姓拼音
    Zhong: '',
    Ming: 'Xiao', //你的名字拼音
    Peixunjigou: '515',
    Peixunjigouming: '北京光环致成国际管理咨询股份有限公司',
    PMIUname: 'email',
    PMIUpass: 'mobile',
    IsPMIUser: false,
    PMINumber: '',
    PMIUtimeB: '',
    PMIUtimeE: '',
    PMItimeB: new Date(1615870735000), //pmi有效期起始时间,用时间戳转换工具
    PMItimeE: new Date(1647406735000), //pmi有效期截止时间,用时间戳转换工具
    Kaodian: '236', //考点id,待获取
    Kaodianming: '天津威训-和平区', //考点名,待确认
    PMIID: '7154257',
}

function trySign(u) {
    SHOW.Ajax.User.Examsign.Sign(
        u.Ed,
        u.Etitle,
        u.Stype,
        u.StypeName,
        u.Xing,
        u.Zhong,
        u.Ming,
        u.Peixunjigou,
        u.Peixunjigouming,
        u.PMIUname,
        u.PMIUpass,
        u.IsPMIUser,
        u.PMINumber,
        u.PMIUtimeB,
        u.PMIUtimeE,
        u.PMItimeB,
        u.PMItimeE,
        u.Kaodian,
        u.Kaodianming,
        u.PMIID,
        res => {
            if (res.value != null) {
                alert("您已报名成功，此次考试您应缴纳的费用为" + res.value + "，您的材料会在3天之内审核，请耐心等待！", "报名提示:", function () {
                    window.location.href = "myexam" + SHOW.Config.Ext;
                });
            } else {
                console.log(`报名失败！AT::${Date.now()}, 重试中...`);
                trySign(u);
            }
        });
}

trySign(signInfo);


// ===============================
// part4 查询
// http://user.chinapmp.cn/myexam.shtml
// ===============================

function appScripts(cb) {
    let _src = scriptArr.shift();
    if (_src) {
        let s = document.createElement('script');
        s.onload = () => {
            console.log(`add script done ==> ${_src}`);
            appScripts(cb);
        };
        s.src = _src;
        document.body.appendChild(s);
    } else {
        console.log('全部注入完成');
        cb();
    }
}

let scriptArr = [
    'http://card.mugeda.com/js/other/jquery.js',
    'http://card.mugeda.com/js/other/juimin.js',
    'http://card.mugeda.com/js/other/jcomm.js',
    'http://card.mugeda.com/js/other/2EA3E9F764EA4B02DDC4C7E109C1C2D9.js',
    'http://card.mugeda.com/js/other/SHOW.Ajax.User.Myexam.js'
];

appScripts(() => {

});


// ===============================
// part5 修改
// http://user.chinapmp.cn/examsignedit.shtml?id=10867719
// ===============================