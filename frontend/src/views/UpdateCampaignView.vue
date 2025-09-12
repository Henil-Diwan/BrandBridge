<script setup>
import { ref, onMounted } from "vue";
import axios from "axios";
import { useRouter, useRoute } from "vue-router";
import { toast } from "vue3-toastify";
import "vue3-toastify/dist/index.css";

let route = useRoute();
let campid = ref(0);
let name = ref("");
let desc = ref("");
let category = ref("");
let end = ref("");
let budget = ref(0);
let goals = ref("");
let visibility = ref("");
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

    const response2 = await axios.get("http://127.0.0.1:5001/update_campaign", {
      params: { campaign_id: route.params.campaign },
    });

    console.log(response2);

    // Extract data from the response and assign it to the respective variables

    const campaignData = response2.data.campaign; // The data you get from the API response
    name.value = campaignData.name;
    desc.value = campaignData.desc;
    category.value = campaignData.category;
    const endDate = new Date(campaignData.end_date); // Convert to JavaScript Date object
    end.value = endDate.toISOString().slice(0, 16);
    budget.value = campaignData.budget;
    goals.value = campaignData.goals;
    visibility.value = campaignData.visibility;
    campid.value = campaignData.id;

    ads.value = response2.data.ads;
  } catch (err) {
    router.push("/login");
  }
});

let goBack = () => {
  router.go(-1);
};

const updateCampaign = async () => {
  const campaignData = {
    campaign_id: route.params.campaign,
    Name: name.value,
    Desc: desc.value,
    Category: category.value,
    End: end.value,
    Budget: budget.value,
    Goals: goals.value,
    Visi: visibility.value,
  };

  try {
    const response_update = await axios.post(
      "http://127.0.0.1:5001/update_campaign",
      campaignData,
      {
        headers: {
          Authorization: `Bearer ${localStorage.getItem("user")?.access_token}`,
        },
      }
    );

    toast("Campaign Update Successfully", {
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

const deleteAd = async (adId) => {
  try {
    const delete_response = await axios.delete(
      `http://127.0.0.1:5001/delete_ad/${adId}`
    );

    toast("Ad Request Deleted Successfully", {
      theme: "auto",
      type: "success",
      dangerouslyHTMLString: true,
      onClose: () => {
        router.go();
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
    console.log(error);
  }
};

</script>

<template>
  <h1>Update Campaign</h1>

  <form @submit.prevent="updateCampaign">
    <div class="mb-3">
      <label for="exampleInputUsername1" class="form-label">Name</label>
      <input
        v-model="name"
        type="text"
        class="form-control"
        id="exampleInputUsername1"
        aria-describedby="usernamelHelp"
      />
    </div>
    <div class="mb-3">
      <label for="exampleInputEmail1" class="form-label">Description</label>
      <input
        v-model="desc"
        type="text"
        class="form-control"
        id="exampleInputEmail1"
        aria-describedby="emailHelp"
      />
    </div>
    <div class="mb-3">
      <label for="exampleInputType1" class="form-label">Category</label>
      <select
        v-model="category"
        class="form-select"
        aria-label="exampleInputType1"
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
    </div>
    <div class="mb-3">
      <label for="exampleInputEmail1" class="form-label">End</label>
      <input
        v-model="end"
        type="datetime-local"
        class="form-control"
        id="exampleInputEmail1"
        aria-describedby="emailHelp"
      />
    </div>
    <div class="mb-3">
      <label for="exampleInputEmail1" class="form-label">Budget</label>
      <input
        v-model="budget"
        type="number"
        class="form-control"
        id="exampleInputEmail1"
        aria-describedby="emailHelp"
      />
    </div>
    <div class="mb-3">
      <label for="exampleInputEmail1" class="form-label">Goals</label>
      <input
        v-model="goals"
        type="text"
        class="form-control"
        id="exampleInputEmail1"
        aria-describedby="emailHelp"
      />
    </div>
    <div class="mb-3">
      <label for="exampleInputType1" class="form-label">Visibility</label>
      <select
        v-model="visibility"
        class="form-select"
        aria-label="exampleInputType1"
      >
        <option value="" disabled selected>Default</option>
        <option value="All">Public</option>
        <option value="None">Private</option>
      </select>
    </div>
    <button type="submit" class="btn btn-primary">Update</button>
  </form>
  <br />

  <h2>Ad Requests</h2>
  <div class="row">
    <div class="col-md-4" v-for="ad in ads" :key="ad.id">
      <div class="card">
        <div class="card-body">
          <p class="card-text">Requirements: {{ ad.requirements }}</p>
          <p class="card-text">Payment: ${{ ad.payment }}</p>
          <router-link :to="'/update_request/' + ad.id" class="btn btn-primary my-5">Update</router-link>
          <button @click="deleteAd(ad.id)" class="btn btn-danger">
            Delete
          </button>
        </div>
      </div>
    </div>
  </div>
  <router-link :to="'/create_request/' + campid" class="btn btn-primary my-5">New Request</router-link>
  <br />
  <button @click="goBack">Back</button>
</template>
