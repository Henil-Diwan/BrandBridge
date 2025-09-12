<script setup>
import { ref } from 'vue';
import axios from 'axios';
import { useRouter } from 'vue-router';
import { toast } from 'vue3-toastify';
import 'vue3-toastify/dist/index.css';


let email = ref('');
let password = ref('');
const router = useRouter();

let loginUser = async () => {
    try {

        const response = await axios.post("http://127.0.0.1:5001/login",{
          email: email.value,
          password: password.value
        });

        console.log(response);
        

        if (response.data.access_token) {
          localStorage.setItem('user', JSON.stringify(response.data));
        }
        
        toast("Login Successful", {
          theme: "auto",
          type: "success",
          dangerouslyHTMLString: true,
          onClose: () => {
            router.push('/');
          },
          autoClose: 1000
        });
        
    } catch (error) {
      console.log(error);
      
      toast(error.response.data.message, {
          theme: "auto",
          type: "error",
          dangerouslyHTMLString: true,
          autoClose: 1000
        });
    }
}

</script>



<template>

<body>
<div class="wrapper">
      <div class="container main">
        <div class="row">
          <div class="col-md-6 side-image">
            <div class="text">
              <p class="h3">BrandBridge</p>
              <p style="font-size: medium">
                Building Bridges between Brands and Influencers
              </p>
            </div>
          </div>

          <div class="col-md-6 right">
            <div class="input-box">
              <header>User Login</header>
              <form @submit.prevent="loginUser">
                <div class="input-field">
                  <input
                  v-model="email"
                    type="text"
                    class="input"
                    id="email"
                    required=""
                    autocomplete="off"
                    name="Email"
                  />
                  <label for="email">Email</label>
                </div>
                <div class="input-field">
                  <input
                  v-model="password"
                    type="password"
                    class="input"
                    id="pass"
                    required=""
                    name="Password"
                  />
                  <label for="pass">Password</label>
                </div>
                <div class="input-field">
                  <input type="submit" class="submit" />
                </div>
              </form>
              <div class="signin">
                <span
                  >Don't have an account?

                  <RouterLink to="/register">Register here</RouterLink></span
                >
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </body>



  </template>

<style scoped>
  @import url("https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap");

* {
  font-family: "Poppins", sans-serif;
}

.wrapper {
  background: #1f1f47;
  padding: 0 20px;
}

.main {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
}

.side-image {
  background-image: linear-gradient(
    45deg,
    #fa709a 0%,
    #fa709a 20%,
    #5c9df1 20%,
    #5c9df1 40%,
    #784ba8 40%,
    #784ba8 60%,
    #fa709a 60%,
    #fa709a 80%,
    #5c9df1 80%,
    #5c9df1 100%
  );
  background-position: center;
  background-size: cover;
  background-repeat: no-repeat;
  border-radius: 10px 0 0 10px;
  position: relative;
}

.row {
  width: 900px;
  height: 550px;
  border-radius: 10px;
  background: white;
  padding: 0;
  box-shadow: 20px 20px 30px 1px rgba(0, 0, 0, 0.2);
}

.text {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}

.text p {
  color: #fff;
  font-size: 20px;
}

i {
  font-weight: 400;
  font-size: 15px;
}

.right {
  display: flex;
  justify-content: center;
  align-items: center;
  position: relative;
}

.input-box {
  width: 330px;
  box-sizing: border-box;
}

img {
  width: 35px;
  position: absolute;
  top: 30px;
  left: 30px;
}

.input-box header {
  font-size: large;
  font-weight: 700;
  text-align: center;
  margin-bottom: 45px;
  color: #1f1f47;
}

.input-field {
  display: flex;
  flex-direction: column;
  position: relative;
  padding: 0 10px;
}

.input {
  height: 45px;
  width: 100%;
  background: transparent;
  border: none;
  border-bottom: 1px solid #1f1f47;
  outline: none;
  margin-bottom: 20px;
  color: #40414a;
}

.input-box .input-field label {
  position: absolute;
  top: 10px;
  left: 10px;
  pointer-events: none;
  transition: 0.5s;
  color: #1f1f47;
}

.input-field input:focus ~ label,
.input-field input:valid ~ label {
  top: -10px;
  font-size: 13px;
  color: #784ba8;
}

.input-field .input:focus,
.input-field .input:valid {
  border-bottom: 1px solid #5c9df1;
}

.submit {
  border: none;
  outline: none;
  height: 45px;
  background: #fa709a;
  border-radius: 5px;
  color: #fff;
  transition: 0.4s;
}

.submit:hover {
  background: #784ba8;
}

.signin {
  text-align: center;
  font-size: small;
  margin-top: 25px;
}

span a {
  text-decoration: none;
  font-weight: 700;
  color: #1f1f47;
  transition: 0.5s;
}

span a:hover {
  text-decoration: underline;
  color: #fa709a;
}

@media only screen and (max-width: 768px) {
  .side-image {
    border-radius: 10px 10px 0 0;
  }

  img {
    width: 35px;
    position: absolute;
    top: 20px;
    left: 47%;
  }

  .text {
    position: absolute;
    top: 70%;
    text-align: center;
  }

  .text p,
  i {
    font-size: 16px;
  }

  .row {
    max-width: 420px;
    width: 100%;
  }
}
</style>
  