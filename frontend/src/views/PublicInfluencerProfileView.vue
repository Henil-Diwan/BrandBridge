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
let current_influencer = ref({});
let current_sponsor = ref({});
let active_campaigns = ref([]);
let ratings = ref([]);
let influencer = ref({});
let selectedCampaigns = ref([]);
let userCampaigns = ref([]);
onMounted(async () => {
  try {
    document.title = `BrandBridge | Influencer`;
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
    const params = { influencer_id: route.params.influencer };
    if (current_user.value.type == "sponsor") {
      params.sponsor_id = current_sponsor.value.id;
    }
    const response2 = await axios.get("http://127.0.0.1:5001/View_influencer", {
      params: params,
    });
    console.log(response2);
    active_campaigns.value = response2.data.active;
    influencer.value = response2.data.influencer;
    ratings.value = response2.data.ratings;
    if (current_user.value.type == "sponsor") {
      userCampaigns.value = response2.data.user_campaigns;
    }
  } catch (err) {
    console.log(err);
    router.push("/login");
  }
});
const flagInfluencer = async (influencerId) => {
  try {
    const response_flag = await axios.post(
      `http://127.0.0.1:5001/flag_influencer/${influencerId}`
    );
    toast("Influencer Flagged!", {
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
const unflagInfluencer = async (influencerId) => {
  try {
    const response_flag = await axios.post(
      `http://127.0.0.1:5001/unflag_influencer/${influencerId}`
    );
    toast("Influencer Unflagged!", {
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
const toggleCampaignSelection = (campaignId) => {
  if (selectedCampaigns.value.includes(campaignId)) {
    selectedCampaigns.value = selectedCampaigns.value.filter(
      (id) => id !== campaignId
    );
  } else {
    selectedCampaigns.value.push(campaignId);
  }
};
const submitRequest = async (infid) => {
  const requestdata = {
    campaign_ids: selectedCampaigns.value,
    influencer_id: infid,
  };
  try {
    const response_update = await axios.post(
      "http://127.0.0.1:5001/request_to_influencer",
      requestdata,
      {
        headers: {
          Authorization: `Bearer ${localStorage.getItem("user")?.access_token}`,
        },
      }
    );
    toast("Requets Sent Successfully", {
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
let chatfunc = () => {
  let person1 = current_user.value.user_id;
  let person2 = influencer.value.created_by;
  let chatter1_id = Math.min(parseInt(person1), parseInt(person2));
  let chatter2_id = Math.max(parseInt(person1), parseInt(person2));
  router.push(`/chat/${chatter1_id}/${chatter2_id}`);
};
</script>
<template>
  <main>
    <div v-if="current_user.type == 'influencer'">
      <InfluencerHeader />
    </div>
    <div v-else-if="current_user.type == 'sponsor'">
      <SponsorHeader />
    </div>
    <div v-else>
      <AdminHeader />
    </div>
    <div class="wrapper my-5">
      <div class="container d-flex justify-content-center">
        <div class="row1">
          <div class="img-container float-end">
            <img
              :src="
                influencer.profile_pic
                  ? `http://127.0.0.1:5001/uploads/${influencer.profile_pic}`
                  : `http://127.0.0.1:5001/uploads/default.png`
              "
              height="200"
              alt="Profile Picture"
              class="rounded"
            />
          </div>
          <div class="details-container mb-5">
            <h3>{{ influencer.name }}</h3>
            <p class="mt-4">{{ influencer.about }}</p>
            <p>Category: {{ influencer.category }}</p>
            <p>Niche: {{ influencer.niche }}</p>
            <p>Reach: {{ influencer.reach }}</p>
            <p>Rating: {{ influencer.rating }}</p>
            <p><i class="bi bi-eye-fill"></i> {{ influencer.views }}</p>
            <div v-if="current_user.type == 'admin'">
              <button
                v-if="influencer.flag === 'No'"
                class="button button-pink"
                @click="flagInfluencer(influencer.id)"
              >
                Flag
              </button>
              <button
                v-else
                class="button button-blue"
                @click="unflagInfluencer(influencer.id)"
              >
                Unflag
              </button>
            </div>
            <div></div>
            <button
              v-if="current_user.type == 'sponsor'"
              type="button"
              class="button button-pink mx-3"
              :data-bs-target="'#requestModal-' + influencer.id"
              data-bs-toggle="modal"
            >
              Request
            </button>
            <button
              v-if="current_influencer.id != influencer.id"
              class="button button-blue"
              @click="chatfunc"
            >
              Chat with Influencer
            </button>
          </div>
          <div class="container">
            <div>
              <h5>Current Campaigns</h5>
            </div>
          </div>
          <div v-if="active_campaigns.length == 0" class="container">
            <div>
              <p class="h6">No Current Campaigns</p>
            </div>
          </div>
          <div v-else class="container">
            <div v-for="campaign in active_campaigns" :key="campaign.id">
              <div
                class="card mb-5 rounded"
                :class="{
                  'card-blue': campaign.id % 3 === 1,
                  'card-pink': campaign.id % 3 === 2,
                  'card-purple': campaign.id % 3 === 0,
                }"
              >
                <div class="card-body p-5">
                  <h4>
                    {{ campaign.name }}
                  </h4>
                  <p class="font-italic text-muted">{{ campaign.desc }}</p>
                  <div class="container">
                    <div class="progress" role="progressbar">
                      <div
                        class="progress-bar"
                        :class="{
                          'bar-blue': campaign.id % 3 === 1,
                          'bar-pink': campaign.id % 3 === 2,
                          'bar-purple': campaign.id % 3 === 0,
                        }"
                        :style="{ width: campaign.completion + '%' }"
                      ></div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div class="comment-container">
            <button
              id="toggleRatingsButton"
              class="button button-blue mt-3"
              type="button"
              data-bs-toggle="collapse"
              data-bs-target="#ratingsCollapse"
              aria-expanded="false"
              aria-controls="ratingsCollapse"
            >
              Ratings
            </button>
            <div class="collapse" id="ratingsCollapse">
              <div class="card card-body mt-3">
                <h4>Ratings</h4>
                <div v-if="ratings">
                  <ul class="list-group">
                    <li v-for="rating in ratings" class="list-group-item">
                      <strong>Rating:</strong> {{ rating.rating }}<br />
                      <strong>Message:</strong> {{ rating.message }}<br />
                      <strong>By:</strong> {{ rating.by }}<br />
                      <strong>At:</strong> {{ rating.rated_at }}
                    </li>
                  </ul>
                </div>
                <div v-else>
                  <p>No ratings available.</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div
      class="modal fade"
      :id="'requestModal-' + influencer.id"
      tabindex="-1"
      aria-labelledby="'requestModalLabel-' + influencer.id"
      aria-hidden="true"
    >
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" :id="'requestModalLabel-' + influencer.id">
              Request to {{ influencer.name }}:
            </h5>
            <button
              type="button"
              class="btn-close"
              data-bs-dismiss="modal"
              aria-label="Close"
            ></button>
          </div>
          <div class="modal-body">
            <div
              v-for="campaign in userCampaigns"
              :key="campaign.id"
              class="form-check"
            >
              <input
                class="form-check-input"
                type="checkbox"
                :id="'campaign-' + campaign.id"
                :value="campaign.id"
                v-model="selectedCampaigns"
              />
              <label class="form-check-label" :for="'campaign-' + campaign.id">
                {{ campaign.name }}
              </label>
            </div>
          </div>
          <div class="modal-footer">
            <button
              type="button"
              class="button button-pink"
              data-bs-dismiss="modal"
            >
              Close
            </button>
            <button
              type="button"
              class="button button-blue"
              @click="submitRequest(influencer.id)"
            >
              Submit Request
            </button>
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
  </main>
</template>
<style scoped>
.card-blue {
  border: 3px solid #5c9df1;
}
.card-pink {
  border: 3px solid #fa709a;
}
.card-purple {
  border: 3px solid #784ba8;
}
.bar-blue {
  background-color: #5c9df1;
}
.bar-pink {
  background-color: #fa709a;
}
.bar-purple {
  background-color: #784ba8;
}
.card {
  color: #40414a;
  font-weight: 500;
}
.back {
  text-align: center;
  font-size: small;
  margin-top: 25px;
}
h4 {
  font-size: large;
}
.ad_card {
  border: 2px solid #784ba887;
  border-radius: 10px;
  overflow: hidden;
  background: white;
  padding: 20px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}
.row1 {
  border-radius: 10px;
  background: white;
  width: 900px;
  padding: 20px;
  box-shadow: 20px 20px 30px 1px rgba(0, 0, 0, 0.2);
}
.button {
  text-decoration: none;
  border-radius: 5px;
  color: white;
  transition: 0.4s;
  margin-top: 35px;
  padding: 7px;
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
  color: white;
}
.comment-input {
  border: 2px solid #784ba887;
}
.change {
  margin-top: 25px;
}
@media only screen and (max-width: 550px) {
  .img-container {
    display: none;
  }
}
</style>
