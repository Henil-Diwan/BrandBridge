<script setup>
import { ref, onMounted } from "vue";
import axios from "axios";
import { useRouter, useRoute } from "vue-router";
import { toast } from "vue3-toastify";
import "vue3-toastify/dist/index.css";
let route = useRoute();
let id = ref(-1);
let name = ref("");
let about = ref("");
let category = ref("");
let niche = ref("");
let reach = ref(0);
let fileInput = ref(null);
let files = ref();
const router = useRouter();
let current_user = ref({
  user_id: 0,
  username: "",
  email: "",
  type: "",
});
let current_influencer = ref({
  id: -1,
  name: "",
  about: "",
  profile_pic: "",
  category: "",
  niche: "",
  reach: 0,
  views: 0,
  rating: 0.0,
  rating_no: 0,
  flag: "",
  created_at: "",
});
function handleFileChange() {
  files.value = fileInput.value?.files;
}
onMounted(async () => {
  try {
    document.title = `BrandBridge | Update Profile`;
    const token = JSON.parse(localStorage.getItem("user"))?.access_token;
    console.log(token);
    if (!token) {
      throw new Error("No token found");
    }
    const response = await axios.get("http://127.0.0.1:5001/protected", {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });
    current_user.value = response.data.logged_in_as;
    current_influencer.value = response.data.current_influencer;
    const response2 = await axios.get(
      "http://127.0.0.1:5001/update_influencer",
      {
        params: { influencer_id: current_influencer.value.id },
      }
    );
    console.log(response2);
    id.value = response2.data.current_influencer.id;
    name.value = response2.data.current_influencer.name;
    about.value = response2.data.current_influencer.about;
    category.value = response2.data.current_influencer.category;
    niche.value = response2.data.current_influencer.niche;
    reach.value = response2.data.current_influencer.reach;
  } catch (err) {
    console.log(err);
    router.push("/login");
  }
});
let updateInfluencer = async () => {
  try {
    const formData = new FormData();
    formData.append("influencer_id", id.value);
    formData.append("name", name.value);
    formData.append("about", about.value);
    formData.append("category", category.value);
    formData.append("niche", niche.value);
    formData.append("reach", reach.value);
    formData.append("creator", route.params.creator);
    const file = files.value ? files.value[0] : null;
    console.log(file);
    if (file) {
      formData.append("ProfilePic", file);
    }
    console.log("selected file", file);
    const response = await axios.post(
      "http://127.0.0.1:5001/update_influencer",
      formData
    );
    console.log(response);
    toast("Influencer Updated Successfully", {
      theme: "auto",
      type: "success",
      dangerouslyHTMLString: true,
      onClose: () => {
        router.push("/influencerhome");
      },
      autoClose: 1000,
    });
  } catch (error) {
    toast("An Error Occured", {
      theme: "auto",
      type: "error",
      dangerouslyHTMLString: true,
      autoClose: 1000,
    });
  }
};
let goBack = () => {
  router.go(-1);
};
</script>
<template>
  <div class="wrapper">
    <div class="container main">
      <div class="row1">
        <div class="input-box">
          <header>Update {{ current_influencer.name }}</header>
          <form method="post" @submit.prevent="updateInfluencer">
            <div class="input-field">
              <input
                v-model="name"
                type="text"
                class="input"
                id="name"
                required=""
                autocomplete="off"
                name="Name"
              />
              <label for="name">Name</label>
            </div>
            <div class="input-field">
              <input
                v-model="about"
                type="text"
                class="input"
                id="about"
                required=""
                autocomplete="off"
                name="About"
              />
              <label for="about">About</label>
            </div>
            <div class="dropdown-wrapper input-field">
              <div>Category</div>
              <select
                v-model="category"
                class="form-control"
                id="dropdown1"
                name="Category"
              >
                <option value="" disabled selected>Default</option>
                <option value="Health & Wellness">Health & Wellness</option>
                <option value="Travel & Food">Travel & Food</option>
                <option value="Finance & Business">Finance & Business</option>
                <option value="Technology">Technology</option>
                <option value="Entertainment">Entertainment</option>
                <option value="Gaming">Gaming</option>
                <option value="Education">Education</option>
                <option value="Lifestyle">Lifestyle</option>
                <option value="Other">Other</option>
              </select>
              <i class="bi bi-caret-down-fill dropdown-icon"></i>
            </div>
            <div class="input-field">
              <input
                v-model="niche"
                type="text"
                class="input"
                id="niche"
                required=""
                autocomplete="off"
                name="Niche"
              />
              <label for="niche">Niche</label>
            </div>
            <div class="input-field">
              <input
                v-model="reach"
                type="number"
                class="input"
                id="reach"
                required=""
                autocomplete="off"
                name="Reach"
              />
              <label for="reach">Number of Followers</label>
            </div>
            <div class="input-field">
              <div>Profile Picture</div>
              <input
                type="file"
                class="input"
                id="pic"
                ref="fileInput"
                @change="handleFileChange"
              />
            </div>
            <div class="input-field">
              <input type="submit" class="submit" value="Update" />
            </div>
            <div class="back text-center mt-4">
              <button type="button" class="back_button" @click="goBack">
                Back
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>
<style scoped>
@import url("https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap");
* {
  font-family: "Poppins", sans-serif;
  margin: 0;
  padding: 0;
}
body {
  margin: 0;
  padding: 0;
}
.wrapper {
  background: #1f1f47;
  padding: 50px;
}
.main {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 90vh;
  min-width: 50vw;
  padding: 50px 20px;
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
  border-radius: 10px;
  position: relative;
}
.row1 {
  width: 50vw;
  border-radius: 10px;
  background: white;
  padding: 20px;
  box-shadow: 20px 20px 30px 1px rgba(0, 0, 0, 0.2);
}
.input-box {
  display: flex;
  flex-direction: column;
  justify-content: center;
}
.input-box header {
  font-size: large;
  font-weight: 700;
  text-align: center;
  margin-bottom: 30px;
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
.dropdown-wrapper {
  position: relative;
  width: 100%;
  margin-bottom: 20px;
}
.dropdown-wrapper select {
  height: 45px;
  width: 100%;
  background: transparent;
  border: none;
  border-bottom: 1px solid #1f1f47;
  padding: 10px;
  color: #40414a;
  outline: none;
  appearance: none;
  font-size: 16px;
}
.dropdown-wrapper .dropdown-icon {
  position: absolute;
  right: 10px;
  top: 50%;
  transform: translateY(-50%);
  font-size: 16px;
  color: #1f1f47;
  pointer-events: none;
}
.submit {
  border: none;
  outline: none;
  height: 45px;
  background: #fa709a;
  border-radius: 5px;
  color: #fff;
  transition: 0.4s;
  margin-top: 20px;
}
.submit:hover {
  background: #784ba8;
}
.btn-update {
  border: none;
  outline: none;
  background: #5c9df1;
  border-radius: 5px;
  color: #fff;
  transition: 0.4s;
  margin-right: 10px;
}
.btn-update:hover {
  background: #784ba8;
  color: #fff;
}
.btn-delete {
  border: none;
  outline: none;
  background: #fa709a;
  border-radius: 5px;
  color: #fff;
  transition: 0.4s;
}
.btn-delete:hover {
  background: #784ba8;
  color: #fff;
}
.back {
  text-align: center;
  font-size: small;
  margin-top: 25px;
}
.back_button {
  border: none;
  background-color: transparent;
  text-decoration: none;
  font-weight: 700;
  color: #1f1f47;
  transition: 0.5s;
  font-size: large;
}
.back_button:hover {
  text-decoration: underline;
  color: #fa709a;
}
.ad-requests-container {
  margin-top: 20px;
}
h4 {
  font-size: large;
}
.ad_card {
  border: 2px solid #784ba887;
  border-radius: 10px;
  overflow: hidden;
  background: white;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}
i {
  font-size: xx-large;
}
.addreq {
  text-decoration: none;
  font-weight: 700;
  color: #1f1f47;
  transition: 0.5s;
  font-size: large;
  background: none;
  padding: 10px 20px;
  border-radius: 5px;
}
.addreq:hover {
  text-decoration: underline;
  color: #fa709a;
}
</style>
