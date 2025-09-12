<script setup>
import { ref, onMounted } from "vue";
import axios from "axios";
import { useRouter, useRoute } from "vue-router";
import { toast } from 'vue3-toastify';
import 'vue3-toastify/dist/index.css';

let route = useRoute();
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
let influencer = ref({});
let rating = ref(0);
let message = ref("");

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

    const response2 = await axios.get("http://127.0.0.1:5001/rate", {
      params: { influencer_id: route.params.influencer }, // Pass user_id as a query parameter
    });

    console.log(response2);

    // Extract data from the response and assign it to the respective variables

    influencer.value = response2.data.rating_influencer;
  } catch (err) {
    console.log(err);
    router.push("/login");
  }
});

let goBack = () => {
  router.go(-1);
};

const createRating = async () => {
  const ratingData = {
    influencer_id: parseInt(route.params.influencer),
    user_id: current_user.value.user_id,
    rating: rating.value,
    message: message.value,
  };
  
  try {
    const response3 = await axios.post(
      "http://127.0.0.1:5001/rate",
      ratingData,  // Send rating data in the body (not as query parameters)
      {
        headers: {
          Authorization: `Bearer ${localStorage.getItem("user")?.access_token}`,
        },
      }
    );

    toast("Rating Created Successfully", {
      theme: "auto",
      type: "success",
      dangerouslyHTMLString: true,
      onClose: () => {
        router.go(-1);
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
  <h1>Rate {{ influencer.name }}</h1>

  <form @submit.prevent="createRating">
    <div class="mb-3">
      <label for="exampleInputUsername1" class="form-label">Rating</label>
      <input
        v-model="rating"
        type="number"
        class="form-control"
        id="exampleInputUsername1"
        aria-describedby="usernamelHelp"
      />
    </div>
    <div class="mb-3">
      <label for="exampleInputEmail1" class="form-label">Message</label>
      <input
        v-model="message"
        type="text"
        class="form-control"
        id="exampleInputEmail1"
        aria-describedby="emailHelp"
      />
    </div>
    
    <button type="submit" class="btn btn-primary">Submit</button>
  </form>
  <br />
  <button @click="goBack">Back</button>
</template>
