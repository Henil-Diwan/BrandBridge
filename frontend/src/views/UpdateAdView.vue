<script setup>
import { ref, onMounted } from "vue";
import axios from "axios";
import { useRouter, useRoute } from "vue-router";
import { toast } from "vue3-toastify";
import "vue3-toastify/dist/index.css";

let req = ref("");
let payment = ref(0);

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

    const response2 = await axios.get("http://127.0.0.1:5001/update_request", {
      params: { ad_id: route.params.ad },
    });

    console.log(response2);

    const adData = response2.data.ad; // The data you get from the API response
    req.value = adData.requirements;
    payment.value = adData.payment;
    
  } catch (err) {
    router.push("/login");
  }
});

let goBack = () => {
  router.push("/");
};

const updateRequest = async () => {
  const adData = {
    ad_id: route.params.ad,
    Requirements: req.value,
    Payment: payment.value,
    };

  try {
    const response_update = await axios.post(
      "http://127.0.0.1:5001/update_request",
      adData,
      {
        headers: {
          Authorization: `Bearer ${localStorage.getItem("user")?.access_token}`,
        },
      }
    );

    toast("Ad Request Update Successfully", {
      theme: "auto",
      type: "success",
      dangerouslyHTMLString: true,
      onClose: () => {
        router.push("/");
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
  <h1>Create Request</h1>

  <form @submit.prevent="updateRequest">
    <div class="mb-3">
      <label for="exampleInputUsername1" class="form-label">Requirements</label>
      <input
        v-model="req"
        type="text"
        class="form-control"
        id="exampleInputUsername1"
        aria-describedby="usernamelHelp"
      />
    </div>

    <div class="mb-3">
      <label for="exampleInputEmail1" class="form-label">Payment</label>
      <input
        v-model="payment"
        type="number"
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
