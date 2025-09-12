<script setup>
import { ref, onMounted } from "vue";
import axios from "axios";
import { useRouter, useRoute } from "vue-router";
import { toast } from "vue3-toastify";
import "vue3-toastify/dist/index.css";
import InfluencerHeader from "@/components/InfluencerHeader.vue";
import SponsorHeader from "@/components/SponsorHeader.vue";
import AdminHeader from "@/components/AdminHeader.vue";

let route = useRoute();

let router = useRouter();
let current_user = ref({
  user_id: 0,
  username: "",
  email: "",
  type: "",
});
let current_sponsor = ref({});
let current_influencer = ref({});
let query = ref("");
let filterType = ref("all");
let filterCategory = ref("");
let results = ref([]);


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
    if (current_user.value.type == "influencer") {
      current_influencer.value = response.data.current_influencer;
    } else if (current_user.value.type == "sponsor") {
      current_sponsor.value = response.data.current_sponsor;
    }

    onSubmit();

  } catch (err) {
    console.log(err);
    
    router.push("/login");
  }
});

const flagCampaign = async (campaignId) => {
  try {
    const response_flag = await axios.post(
      `http://127.0.0.1:5001/flag_campaign/${campaignId}`
    );
    toast("Campaign Flagged!", {
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

const unflagCampaign = async (campaignId) => {
  try {
    const response_flag = await axios.post(
      `http://127.0.0.1:5001/unflag_campaign/${campaignId}`
    );
    toast("Campaign Unflagged!", {
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

let onSubmit = async () => {
    try {
        const response = await axios.get('http://127.0.0.1:5001/search', {
          params: {
            q: query.value,
            filter: filterType.value,
            category: filterCategory.value,
          },
        });
        results.value = response.data;
      } catch (error) {
        console.error('Error fetching search results:', error);
      }
}
</script>

<template>
  <div v-if="current_user.type == 'influencer'">
    <InfluencerHeader />
  </div>
  <div v-else-if="current_user.type == 'sponsor'">
    <SponsorHeader />
  </div>
  <div v-else>
    <AdminHeader />
  </div>


  <div class="container my-5">
      <h3>Search Results for "{{ query }}":</h3>
    </div>

    <div class="container mb-5">
      <form @submit.prevent="onSubmit">
        <div class="input-field">
          <input v-model="query" type="text" class="input" required autocomplete="off" name="q" />
          <label for="query">Search</label>
        </div>
        <div class="dropdown-wrapper">
          <select v-model="filterType" class="form-control" id="filter" name="filter">
            <option value="all">All</option>
            <option value="campaign">Campaigns</option>
            <option value="influencer">Influencers</option>
          </select>
        </div>
        <div class="dropdown-wrapper">
          <select v-model="filterCategory" class="form-control" id="category" name="category">
            <option value="">All Categories</option>
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
        <button type="submit" class="submit">Search</button>
      </form>
    </div>

    <div v-if="results.length === 0" class="my-5 text-center text-white">
      <h3>No Results found</h3>
    </div>

    <div v-else class="container">
      <div class="row gap-5 justify-content-start">
        <div v-for="(result, index) in results" :key="index" class="col-md-8 col-lg-3 mb-4 bg">
          <div v-if="result.type === 'campaign'" class="card" style="width: 100%">
            <div class="card-body">
              <p class="card-text">{{ result.object.Created_by_name }}  </p>
              <h5 class="card-title"><router-link :to="'/show_campaign/' + result.object.Campaign_ID" class="link-dark">{{ result.object.Name }} </router-link></h5>
              <p class="card-text">{{ result.object.Desc.substring(0, 50) }}...</p>
            </div>
            <ul class="list-group list-group-flush">
              <li class="list-group-item">Preferred Category: {{ result.object.Preferred_Category }}</li>
              <li class="list-group-item">Goals: {{ result.object.Goals }}</li>
              <li class="list-group-item">Total Budget: {{ result.object.Budget }}</li>
              <li class="list-group-item">From: {{ result.object.Start_Date }} To: {{ result.object.End_Date }}</li>
              <li class="list-group-item">Views: {{ result.object.Views }}</li>
            </ul>
            <div class="card-body text-center">
              <router-link :to="'/show_campaign/' + result.object.Campaign_ID" class="btn btn-primary">View Requests</router-link>
            </div>
          </div>

          <div v-if="result.type === 'influencer'" class="card">
            <div class="card-body">
              <h5 class="card-title">
                <router-link :to="'/view_influencer/' + result.object.Infuencer_ID" class="link-dark">{{ result.object.Name }}</router-link>
              </h5>
              <p class="card-text">{{ result.object.About }}</p>
            </div>
            <ul class="list-group list-group-flush">
              <li class="list-group-item">Category: {{ result.object.Category }}</li>
              <li class="list-group-item">Niche: {{ result.object.Niche }}</li>
              <li class="list-group-item">Reach: {{ result.object.Reach }}</li>
              <li class="list-group-item">Views: {{ result.object.Views }}</li>
            </ul>
            <div class="card-body">
              <router-link :to="'/view_influencer/' + result.object.Infuencer_ID" class="btn btn-primary">View Profile</router-link>
            </div>
          </div>
        </div>
      </div>
    </div>
  
  <br />
</template>
