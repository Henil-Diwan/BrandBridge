<script setup>
import { ref, onMounted } from "vue";
import axios from "axios";
import { useRouter, useRoute } from "vue-router";
import { toast } from "vue3-toastify";
import "vue3-toastify/dist/index.css";
import InfluencerHeader from "@/components/InfluencerHeader.vue";
import SponsorHeader from "@/components/SponsorHeader.vue";
import AdminHeader from "@/components/AdminHeader.vue";
import SponsorFooter from "@/components/SponsorFooter.vue";
import InfluencerFooter from "@/components/InfluencerFooter.vue";
import AdminFooter from "@/components/AdminFooter.vue";
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
    document.title = `BrandBridge | Search`;
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
    const response = await axios.get("http://127.0.0.1:5001/search", {
      params: {
        q: query.value,
        filter: filterType.value,
        category: filterCategory.value,
      },
    });
    results.value = response.data;
  } catch (error) {
    console.error("Error fetching search results:", error);
  }
};
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
  <div class="container">
    <div class="my-5 text-white">
      <h3>Search Results for "{{ query }}":</h3>
    </div>
  </div>
  <div class="container mb-5">
    <div class="input-box">
      <form @submit.prevent="onSubmit">
        <div class="input-field d-block d-md-inline-block">
          <input
            v-model="query"
            type="text"
            class="input"
            id="query"
            required=""
            autocomplete="off"
          />
          <label for="query">Search</label>
        </div>
        <div class="dropdown-wrapper d-block d-md-inline-block input-field">
          <select
            v-model="filterType"
            class="form-control"
            id="filter"
            name="filter"
          >
            <option value="all">All</option>
            <option value="campaign">Campaigns</option>
            <option value="influencer">Influencers</option>
          </select>
        </div>
        <div class="dropdown-wrapper d-block d-md-inline-block input-field">
          <select
            v-model="filterCategory"
            class="form-control"
            id="category"
            name="category"
          >
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
        <input type="submit" class="submit" value="Search" />
      </form>
    </div>
  </div>
  <div v-if="results.length === 0" class="my-5 text-center text-white">
    <h3>No Results found</h3>
  </div>
  <div v-else class="container">
    <div class="row gap-5 justify-content-start">
      <div
        v-for="(result, index) in results"
        :key="index"
        class="col-md-8 col-lg-3 mb-4 bg"
      >
        <div v-if="result.type === 'campaign'" class="card" style="width: 100%">
          <div class="card-body">
            <p class="card-text">{{ result.object.Created_by_name }}</p>
            <h5 class="card-title">
              <router-link
                :to="'/show_campaign/' + result.object.Campaign_ID"
                class="link-dark"
                >{{ result.object.Name }}
              </router-link>
            </h5>
            <p class="card-text">
              {{ result.object.Desc.substring(0, 50) }}...
            </p>
          </div>
          <ul class="list-group list-group-flush">
            <li class="list-group-item">
              Preferred Category: {{ result.object.Preferred_Category }}
            </li>
            <li class="list-group-item">Goals: {{ result.object.Goals }}</li>
            <li class="list-group-item">
              Total Budget: {{ result.object.Budget }}
            </li>
            <li class="list-group-item">
              From: {{ result.object.Start_Date }} To:
              {{ result.object.End_Date }}
            </li>
            <li class="list-group-item">Views: {{ result.object.Views }}</li>
          </ul>
          <div class="card-body text-center">
            <router-link
              :to="'/show_campaign/' + result.object.Campaign_ID"
              class="button button-blue"
              >View Requests</router-link
            >
          </div>
        </div>
        <div v-if="result.type === 'influencer'" class="card">
          <div class="card-body">
            <h5 class="card-title">
              <router-link
                :to="'/view_influencer/' + result.object.Infuencer_ID"
                class="link-dark"
                >{{ result.object.Name }}</router-link
              >
            </h5>
            <p class="card-text">{{ result.object.About }}</p>
          </div>
          <ul class="list-group list-group-flush">
            <li class="list-group-item">
              Category: {{ result.object.Category }}
            </li>
            <li class="list-group-item">Niche: {{ result.object.Niche }}</li>
            <li class="list-group-item">Reach: {{ result.object.Reach }}</li>
            <li class="list-group-item">Views: {{ result.object.Views }}</li>
          </ul>
          <div class="card-body text-center">
            <router-link
              :to="'/view_influencer/' + result.object.Infuencer_ID"
              class="button button-blue"
              >View Profile</router-link
            >
          </div>
        </div>
      </div>
    </div>
  </div>
  <div v-if="current_user.type == 'influencer'">
    <InfluencerFooter />
  </div>
  <div v-else-if="current_user.type == 'sponsor'">
    <SponsorFooter />
  </div>
  <div v-else>
    <AdminFooter />
  </div>
</template>
<style scoped>
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
.input-box {
  display: flex;
  flex-direction: column;
  justify-content: center;
}
.input-field {
  display: flex;
  flex-direction: column;
  position: relative;
  padding: 0 10px;
  width: 40%;
}
.input {
  height: 45px;
  width: 100%;
  font-size: 20px;
  background: transparent;
  border: none;
  border-bottom: 1px solid white;
  outline: none;
  margin-bottom: 20px;
  color: white;
}
.input-box .input-field label {
  position: absolute;
  top: 10px;
  left: 10px;
  pointer-events: none;
  transition: 0.5s;
  color: white;
}
.input-field input:focus ~ label,
.input-field input:valid ~ label {
  top: -20px;
  font-size: 20px;
  color: white;
}
.input-field .input:focus,
.input-field .input:valid {
  border-bottom: 1px solid white;
}
.dropdown-wrapper {
  position: relative;
  width: 20%;
  margin-bottom: 20px;
}
.dropdown-wrapper select {
  height: 45px;
  width: 100%;
  background: transparent;
  border: none;
  border-bottom: 1px solid white;
  padding: 10px;
  color: white;
  outline: none;
  appearance: none;
  font-size: 16px;
}
.dropdown-wrapper select:focus {
  color: black;
  background-color: white;
}
.dropdown-wrapper .dropdown-icon {
  position: absolute;
  right: 10px;
  top: 50%;
  transform: translateY(-50%);
  font-size: 16px;
  color: white;
  pointer-events: none;
}
.submit {
  border: none;
  padding: 10px;
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
span a {
  text-decoration: none;
  font-weight: 700;
  color: hsl(240, 39%, 20%);
  transition: 0.5s;
}
span a:hover {
  text-decoration: underline;
  color: #fa709a;
}
@media only screen and (max-width: 768px) {
  .dropdown-wrapper {
    width: 100%;
  }
  .input-field {
    width: 100%;
  }
}
</style>
