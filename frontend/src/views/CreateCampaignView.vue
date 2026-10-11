<script setup>
import { ref, onMounted } from "vue";
import axios from "axios";
import { useRouter } from "vue-router";
import { toast } from "vue3-toastify";
import "vue3-toastify/dist/index.css";
let name = ref("");
let desc = ref("");
let category = ref("");
let start = ref("");
let end = ref("");
let budget = ref(0);
let goals = ref("");
let visibility = ref("");
let router = useRouter();
let current_user = ref({
  user_id: 0,
  username: "",
  email: "",
  type: "",
});
let current_sponsor = ref({
  id: -1,
  name: "",
  budget: 0,
  industry: "",
  flag: "",
  created_at: "",
});
onMounted(async () => {
  try {
    document.title = `BrandBridge | Create Campaign`;
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
    current_sponsor.value = response.data.current_sponsor;
    console.log(current_sponsor.value);
  } catch (err) {
    router.push("/login");
  }
});
let goBack = () => {
  router.go(-1);
};
const createCampaign = async () => {
  const campaignData = {
    Name: name.value,
    Desc: desc.value,
    Category: category.value,
    Start: start.value,
    End: end.value,
    Budget: budget.value,
    Goals: goals.value,
    Visi: visibility.value,
    Created_by: current_sponsor.value.id,
  };
  try {
    const response2 = await axios.post(
      "http://127.0.0.1:5001/create_campaign",
      campaignData,
      {
        headers: {
          Authorization: `Bearer ${localStorage.getItem("user")?.access_token}`,
        },
      }
    );
    toast("Campaign Created Successfully", {
      theme: "auto",
      type: "success",
      dangerouslyHTMLString: true,
      onClose: () => {
        router.push(`/create_request/${response2.data.Campaign_ID}`);
      },
      autoClose: 1000,
    });
  } catch (err) {
    console.log(err);
    toast("An Error Occured", {
      theme: "auto",
      type: "error",
      dangerouslyHTMLString: true,
      autoClose: 1000,
    });
  }
};
</script>
<template>
  <div class="wrapper">
    <div class="container main">
      <div class="row">
        <div class="input-box">
          <header>Create a Campaign</header>
          <form @submit.prevent="createCampaign">
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
                v-model="desc"
                type="text"
                class="input"
                id="Desc"
                required=""
                autocomplete="off"
                name="Desc"
              />
              <label for="Desc">Description</label>
            </div>
            <div class="dropdown-wrapper input-field">
              <select
                v-model="category"
                class="form-control"
                id="dropdown1"
                name="Category"
              >
                <option value="" disabled selected>Default</option>
                <option value="Any">Any</option>
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
              <div>Start Date</div>
              <input
                v-model="start"
                type="datetime-local"
                class="input"
                id="Start"
                required=""
                autocomplete="off"
                name="Start"
              />
            </div>
            <div class="input-field">
              <div>End Date</div>
              <input
                v-model="end"
                type="datetime-local"
                class="input"
                id="End"
                required=""
                autocomplete="off"
                name="End"
              />
            </div>
            <div class="input-field">
              <input
                v-model="budget"
                type="number"
                class="input"
                id="Budget"
                required=""
                autocomplete="off"
                name="Budget"
              />
              <label for="Budget">Budget</label>
            </div>
            <div class="input-field">
              <input
                v-model="goals"
                type="text"
                class="input"
                id="Goals"
                required=""
                autocomplete="off"
                name="Goals"
              />
              <label for="Goals">Goals</label>
            </div>
            <div class="dropdown-wrapper input-field">
              <div>Visibility</div>
              <select
                v-model="visibility"
                class="form-control"
                id="dropdown1"
                name="Visi"
              >
                <option value="" disabled selected>Default</option>
                <option value="All">Public</option>
                <option value="None">Private</option>
              </select>
              <i class="bi bi-caret-down-fill dropdown-icon"></i>
            </div>
            <div class="input-field">
              <input type="submit" class="submit" value="Create" />
            </div>
          </form>
          <div class="back">
            <button class="back_button" @click="goBack">Back</button>
          </div>
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
.row {
  width: 100%;
  max-width: 500px;
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
.back {
  text-align: center;
  font-size: small;
  margin-top: 25px;
}
@media only screen and (max-width: 768px) {
  .row {
    width: 100%;
    padding: 15px;
  }
}
.back_button {
  background-color: transparent;
  border: none;
  text-decoration: none;
  font-weight: 700;
  color: hsl(240, 39%, 20%);
  transition: 0.5s;
}
.back_button:hover {
  text-decoration: underline;
  color: #fa709a;
}
</style>
