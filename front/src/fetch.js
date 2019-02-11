import axios from "axios";
import _ from "lodash";

// import { Message, MessageBox, Loading } from "element-ui";
// import router from "@/router";
import store from "@/store";

function paramsSerializer(params) {
  let parts = [];
  for (let key in params) {
    let val = params[key];
    if (val === null || typeof val === "undefined") {
      continue;
    }
    if (Array.isArray(val)) {
      val = JSON.stringify(val);
    }
    parts.push(encodeURIComponent(key) + "=" + encodeURIComponent(val));
  }
  let result = parts.join("&");
  return result;
};
axios.defaults.headers.post["Content-Type"] = "application/x-www-form-urlencoded";

let instance = axios.create({
  baseURL: "/api",
  // timeout: 600000,
  timeout: 100000,
  paramsSerializer: function (params) {
    return paramsSerializer(params);
  }
});

function paramPost(data) {
  var params = new URLSearchParams();
  for (let name in data) {
    params.append(name, data[name]);
  }
  return params;
};

function _showError(msg,isShow=true) {
  /* if (isShow) {
    Message.error({
      message: msg
    })
  } */
}
/*
var loadinginstace;
let needLoadingRequestCount = 0
 function showLoading(isShow=true) {
  if (isShow) {
    if (needLoadingRequestCount === 0) {
      loadinginstace = Loading.service({
        lock: true,
        text: '加载中……',
        background: 'rgba(0, 0, 0, 0.7)'
      })
    }
    needLoadingRequestCount++
  }
  
} 
function tryHideLoading(isShow=true) {//debugger
  if (isShow) {
    if (needLoadingRequestCount <= 0) return
    needLoadingRequestCount--
    _.debounce(() => {
      if (needLoadingRequestCount === 0) {
        loadinginstace.close()
      }
    }, 300)()
    
  }
}
*/
//request请求拦截器
instance.interceptors.request.use(config => {
  // console.log('config',config)
  // showLoading(config.showLoading)
  return config
}, error => {
  // tryHideLoading(config.showLoading)
  // _showError('加载超时');
  return Promise.reject(error)
})

//response响应拦截器
instance.interceptors.response.use(res => {//debugger
  // tryHideLoading(res.config.showLoading);
  let isShowMsg = res.config.showMsg;
  let resData = res.data;
  return resData;
  if (res.status == 200) {
    
    /* if (res.config.url == "/api/user/loginstatus" && res.data.code == 0) {
      //登陆成功后对保存过期状态
      localStorage.setItem("isExpires", "1"); //0过期，1不过期
    } */
    if (Object.prototype.toString.call(resData) === "[object Object]") {
      // if (resData.hasOwnProperty("code")) {
        if (resData.code == 0) {
          return resData.data;
        } else {
          _showError(resData.msg, isShowMsg);
          return Promise.reject(new Error(resData.msg));
        }
      // } else {
        // _showError('request.data.code does not exist');
        // console.error("request.data.code does not exist");
        // return Promise.reject(new Error("服务器异常，请联系系统管理员！"));
        // return Promise.reject(new Error("request.data.ret does not exist"));
      // }
    } else {
      _showError('request.data is not Object');
      console.error("request.data is not Object");
      return Promise.reject(new Error("服务器异常，请联系系统管理员！"));
      // return Promise.reject(new Error("request.data is not Object"));
    }
  } else if(res.status == 403){
    /* MessageBox({
      title: "提示",
      message: "登录信息过期，请重新登录",
      confirmButtonText: "确定",
      callback: action => {
        store.dispatch("user/remove_login_info").then(() => {
          // isLogonExpires = false;
          router.push("/login");
        });
      }
    }); */
  }else{
    _showError('服务器异常');
  }

}, error => {
    // tryHideLoading();

    if (error.response.status == 504) {
      /* MessageBox({
        title: "提示",
        message: error.response.statusText,
        confirmButtonText: "确定"
      }); */
    }
    //403过期
    if (error.response.status == 403) {
      /* MessageBox({
        title: "提示",
        message: "登录信息过期，请重新登录",
        confirmButtonText: "确定",
        callback: action => {
          store.dispatch("user/remove_login_info").then(() => {
            router.push("/login");
          });
        }
      }); */
    }
  
  return Promise.reject(error)
});

let _get = instance.get
let _delete = instance.delete
let _post = instance.post
let _put = instance.put

function handleParams(arr) {
  let url = arr[0];
  let id = arr[1];
  let data = _.isPlainObject(arr[2])?arr[2]:{};
  let option = _.isPlainObject(arr[3])?arr[3]:{};
  /* if (!url.endsWith("/")) {
    url = url+"/"
  } */
  if (id) {
    let idStr = id;
    url = url + idStr;
  }

  arr[0] = url;
  arr[1] = data
  arr[2] = option
  arr.length = 3;
  return arr
}
/**
 * 第一个参数url  string
 * 第二个参数get对于的id，为空传‘’  string或者number
 * 第三个参数查询参数对象  object
 * 第四个参数option  object
 */
instance.put = function(...params) {
  let _params = handleParams(params);
  return _put(..._params);
}
/**
 * 第一个参数url  string
 * 第二个参数get对于的id，为空传‘’  string或者number
 * 第三个参数查询参数对象  object
 * 第四个参数option  object
 */
instance.post = function (...params) {
  let _params = handleParams(params);
  return _post(..._params);
}
/**
 * 第一个参数url  string
 * 第二个参数get对于的id，为空传‘’  string或者number
 * 第三个参数查询参数对象  object
 * 第四个参数option  object
 */
instance.get = function(...params) {
  let _params = handleParams(params);
  _params[1] = {
    params: _params[1],
    ..._params[2]
  }
  params.length=2;
  return _get(..._params);
}

/**
 * 第一个参数url  string
 * 第二个参数get对于的id，为空传‘’  string或者number
 * 第三个参数option  object
 */
instance.delete = function(...params) {
  let _params = handleParams(params);
  _params.length = 2;
  return _delete(..._params);
}

export default instance;
