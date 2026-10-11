<script setup>
import { ref, onMounted } from "vue";
import axios from "axios";
import { useRouter, useRoute } from "vue-router";
import { toast } from "vue3-toastify";
import "vue3-toastify/dist/index.css";
let route = useRoute();
let ads = ref([]);
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
    document.title = `BrandBridge | Change Campaign`;
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
    const response2 = await axios.get("http://127.0.0.1:5001/change_campaign", {
      params: { campaign_id: route.params.campaign },
    });
    console.log(response2);
    ads.value = response2.data.ads;
  } catch (err) {
    router.push("/login");
  }
});
let goBack = () => {
  router.go(-1);
};
const markAd = async (adId) => {
  try {
    const response_mark = await axios.post(
      `http://127.0.0.1:5001/mark_ad/${adId}`
    );
    toast("Ad Marked!", {
      theme: "auto",
      type: "success",
      dangerouslyHTMLString: true,
      onClose: () => {
        router.go();
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
const undoAd = async (adId) => {
  try {
    const response_mark = await axios.post(
      `http://127.0.0.1:5001/undo_ad/${adId}`
    );
    toast("Ad Unmarked!", {
      theme: "auto",
      type: "success",
      dangerouslyHTMLString: true,
      onClose: () => {
        router.go();
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
      <div class="row1">
        <div class="input-box">
          <header>Change Request Status</header>
          <div class="ad-requests-container">
            <h4>Ad Requests</h4>
            <div class="row">
              <h4 v-if="ads.length == 0">No Current Requests</h4>
              <div
                v-else
                v-for="(ad, index) in ads"
                :key="ad.id"
                class="col-md-6 mb-3"
              >
                <div class="ad_card">
                  <div class="card-body">
                    <p class="card-text">{{ ad.requirements }}</p>
                    <p class="card-text">Amount: {{ ad.payment }}</p>
                    <p class="card-text">Date: {{ ad.time }}</p>
                    <p class="card-text">
                      Status: <strong> {{ ad.status }} </strong>
                    </p>
                    <button
                      v-if="ad.status == 'Completed'"
                      @click="undoAd(ad.id)"
                      class="button button-pink"
                    >
                      Undo
                    </button>
                    <button
                      v-else
                      @click="markAd(ad.id)"
                      class="button button-blue"
                    >
                      Mark as Done
                    </button>
                  </div>
                </div>
              </div>
              <div v-if="(index + 1) % 2 === 0" class="w-100"></div>
            </div>
          </div>
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
  padding: 3%;
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
.card {
  color: #40414a;
  font-weight: 500;
}
.button {
  text-decoration: none;
  border-radius: 5px;
  color: white;
  transition: 0.4s;
  margin-top: 35px;
  padding: 5px;
  border: none;
}
.button-pink {
  background: #fa709a;
}
.button-blue {
  background: #5c9df1;
}
.button:hover {
  background: #784ba8;
}
</style>
