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

    // Extract data from the response and assign it to the respective variables

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
    const response_mark = await axios.post(`http://127.0.0.1:5001/mark_ad/${adId}`);
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
    const response_mark = await axios.post(`http://127.0.0.1:5001/undo_ad/${adId}`);
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
  <h1>Change Campaign: </h1>

  <h2>Ad Requests</h2>
  <div class="row">
    <div class="col-md-4" v-for="ad in ads" :key="ad.id">
      <div class="card">
        <div class="card-body">
          <p class="card-text">Requirements: {{ ad.requirements }}</p>
          <p class="card-text">Payment: ${{ ad.payment }}</p>
          <p class="card-text">Status: {{ ad.status }}</p>
          
          <button v-if="ad.status == 'Completed'" @click="undoAd(ad.id)" class="btn btn-danger">
            Undo
          </button>
          <button v-else @click="markAd(ad.id)" class="btn btn-primary">
            Mark as Done
          </button>

        </div>
      </div>
    </div>
  </div>
  <br />
  <button @click="goBack">Back</button>
</template>
