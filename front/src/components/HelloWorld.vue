<template>
  <div class="hello">
    <h1>{{ msg }}</h1>
    <button @click="onClickLogin">post-"login" 登录</button>
    <button @click="onClickLogout">post-"logout" 登出</button>
    <button @click="onClick1">get-"todos" 查询所有</button>

    <button @click="onClick2">get-"todos/todo_id" 查询指定</button>

    <button @click="onClick3">put-"todos/todo_id" 新增</button>
    
    <p>response==</p>
    {{response}}
    <!-- <vue-json-pretty
      :path="'res'"
      :showLength='true'
      :data="response">
    </vue-json-pretty> -->

    <!-- <vue-json-viewer
      :value="response"
      :expand-depth=5
      copyable
      boxed
      sort>
    </vue-json-viewer> -->
  </div>
</template>

<script>
import fetch from "@/fetch";
export default {
  name: "HelloWorld",
  components: {
  },
  props: {
    msg: String
  },
  data() {
    return {
      response:{}
    }
  },
  methods: {
    //生成1-int之间的一个随机数。
    getRandom(int){
      return Math.ceil(Math.random()*int);
    },
    async onClickLogin(){
      let obj = {
        username:'Mayue',
        password:'123456',
      }
      let data = await fetch.post('/login','',obj);
      this.response = data;
      console.log(data)
    },
    async onClickLogout(){
      let data = await fetch.post('/logout');
      this.response = data;
      console.log(data)
    },
    async onClick1(){
      let data = await fetch.get('/users');
      this.response = data;
      console.log(data)
    },
    async onClick2(){
      let num = this.getRandom(3);
      // for
      num = 2;
      let id = 'todo'+num;
      let data = await fetch.get('/users/',3,{username:'34',email:'500@qq.com'});
      this.response = data;
      console.log(data)
    },
    async onClick3(){
      let id = _.uniqueId('new_')
      let age = [23,34,66,'33'];
      let name = '马越';
      let info = {level:'2',type:'0'};
      let data = await fetch.post('/todos','',{'task': id,age,info});
      this.response = data;
      console.log(data)
    },
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h3 {
  margin: 40px 0 0;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>
