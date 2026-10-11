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
let comments = ref([]);
let campaign = ref({});
let ads = ref([]);
let message = ref("");
let id = ref(0);
onMounted(async () => {
  try {
    document.title = `BrandBridge | Campaign`;
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
      id.value = current_influencer.value.id;
    } else if (current_user.value.type == "sponsor") {
      current_sponsor.value = response.data.current_sponsor;
      id.value = current_sponsor.value.id;
    }
    const params = { campaign_id: route.params.campaign };
    if (current_user.value.type == "influencer") {
      params.influencer_id = current_influencer.value.id;
    }
    const response2 = await axios.get("http://127.0.0.1:5001/show_campaign", {
      params: params,
    });
    console.log(response2);
    comments.value = response2.data.messages;
    campaign.value = response2.data.campaign;
    ads.value = response2.data.ads;
  } catch (err) {
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
let createComment = async () => {
  try {
    const response_comment = await axios.post(
      "http://127.0.0.1:5001/create_comment",
      {
        message: message.value,
        type: current_user.value.type,
        campaign: route.params.campaign,
        id: id.value,
      }
    );
    toast("Comment Creeated Successfully", {
      theme: "auto",
      type: "success",
      dangerouslyHTMLString: true,
      onClose: () => {
        router.go();
      },
      autoClose: 1000,
    });
  } catch (error) {
    console.log(error);
    toast("An Error Occured", {
      theme: "auto",
      type: "error",
      dangerouslyHTMLString: true,
      autoClose: 1000,
    });
  }
};
const submitRequest = async (campaign_id) => {
  const requestdata = {
    campaign_id: campaign_id,
    influencer_id: current_influencer.value.id,
  };
  try {
    const response_request = await axios.post(
      "http://127.0.0.1:5001/request_by_influencer",
      requestdata,
      {
        headers: {
          Authorization: `Bearer ${localStorage.getItem("user")?.access_token}`,
        },
      }
    );
    toast("Request Sent Successfully", {
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
const saveCampaign = async (campaign_id) => {
  const requestdata = {
    campaign_id: campaign_id,
    influencer_id: current_influencer.value.id,
  };
  try {
    const save_response = await axios.post(
      "http://127.0.0.1:5001/save_campaign",
      requestdata,
      {
        headers: {
          Authorization: `Bearer ${localStorage.getItem("user")?.access_token}`,
        },
      }
    );
    toast("Campaign Saved Successfully", {
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
const unsaveCampaign = async (campaign_id) => {
  const requestdata = {
    campaign_id: campaign_id,
    influencer_id: current_influencer.value.id,
  };
  try {
    const unsave_response = await axios.post(
      "http://127.0.0.1:5001/unsave_campaign",
      requestdata,
      {
        headers: {
          Authorization: `Bearer ${localStorage.getItem("user")?.access_token}`,
        },
      }
    );
    toast("Campaign Unsaved Successfully", {
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
  let person2 = campaign.value.created_by_user_id;
  let chatter1_id = Math.min(parseInt(person1), parseInt(person2));
  let chatter2_id = Math.max(parseInt(person1), parseInt(person2));
  router.push(`/chat/${chatter1_id}/${chatter2_id}`);
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
  <div class="wrapper my-5">
    <div class="container d-flex justify-content-center">
      <div class="row1">
        <div class="details-container mb-5">
          <p>{{ campaign.created_by_name }}</p>
          <h3>{{ (campaign.name, e) }}</h3>
          <p class="mb-3">{{ campaign.desc }}</p>
          <p>Preferred Category: {{ campaign.category }}</p>
          <p>Start Date: {{ campaign.start_date }}</p>
          <p>End Date: {{ campaign.end_date }}</p>
          <p>Goals: {{ campaign.goals }}</p>
          <p>Budget: {{ campaign.budget }}</p>
          <p><i class="bi bi-eye-fill"></i> {{ campaign.views }}</p>
        </div>
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
                  <p class="card-text">Date: {{ ad.created_at }}</p>
                  <p class="card-text">Status: {{ ad.status }}</p>
                </div>
                <button
                  v-if="
                    current_user.type == 'sponsor' &&
                    current_sponsor.id == campaign.created_by &&
                    ad.status == 'Completed'
                  "
                  type="button"
                  class="button button-blue"
                  data-bs-toggle="modal"
                  data-bs-target="#exampleModal"
                >
                  Pay
                </button>
              </div>
            </div>
          </div>
          <div v-if="(index + 1) % 2 === 0" class="w-100"></div>
        </div>
        <div class="comment-container">
          <button
            id="toggleCommentsButton"
            class="button button-pink"
            type="button"
            data-bs-toggle="collapse"
            data-bs-target="#commentsCollapse"
            aria-expanded="false"
            aria-controls="commmentssCollapse"
          >
            Comments
          </button>
          <div class="collapse" id="commentsCollapse">
            <div class="card card-body mt-3">
              <h4>Comments</h4>
              <form @submit.prevent="createComment">
                <div class="mb-3">
                  <input
                    v-model="message"
                    type="text"
                    class="form-control"
                    id="exampleInputUsername1"
                    aria-describedby="usernamelHelp"
                  />
                </div>
                <button type="submit" class="button button-blue">Submit</button>
              </form>
              <div v-if="comments.length > 0">
                <ul class="list-group">
                  <li v-for="message in comments" class="list-group-item">
                    <strong>From: </strong> {{ message.from }}<br />
                    <strong>At:</strong> {{ message.date }} <br />
                    <strong>Message:</strong>
                    {{ message.message }}<br />
                  </li>
                </ul>
              </div>
              <div v-else>
                <p>No commments available.</p>
              </div>
            </div>
          </div>
        </div>
        <div>
          <button
            v-if="current_sponsor.id != campaign.created_by"
            class="button button-blue"
            @click="chatfunc"
          >
            Chat With Sponsor
          </button>
        </div>
        <div v-if="current_user.type == 'influencer'">
          <button
            class="button button-pink"
            @click="submitRequest(campaign.id)"
          >
            Request
          </button>
          <br />
          <button
            v-if="campaign.saved"
            type="button"
            class="button button-pink"
            @click="unsaveCampaign(campaign.id)"
          >
            Unsave
          </button>
          <button
            v-else
            type="button"
            class="button button-blue"
            @click="saveCampaign(campaign.id)"
          >
            Save
          </button>
        </div>
        <div v-if="current_user.type == 'admin'">
          <button
            v-if="campaign.flag === 'No'"
            class="button button-pink"
            @click="flagCampaign(campaign.id)"
          >
            Flag
          </button>
          <button
            v-else
            class="button button-blue"
            @click="unflagCampaign(campaign.id)"
          >
            Unflag
          </button>
        </div>
      </div>
    </div>
  </div>
  <div
    class="modal fade"
    id="exampleModal"
    tabindex="-1"
    aria-labelledby="exampleModalLabel"
    aria-hidden="true"
  >
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h1 class="modal-title fs-5" id="exampleModalLabel">Payment</h1>
          <button
            type="button"
            class="btn-close"
            data-bs-dismiss="modal"
            aria-label="Close"
          ></button>
        </div>
        <div class="modal-body">
          <div class="card px-4">
            <p class="h8 py-3">Payment Details</p>
            <div class="row">
              <div class="d-flex flex-column">
                <p class="text mb-1">Person Name</p>
                <input
                  class="form-control mb-3"
                  type="text"
                  placeholder="Name"
                  value="Henil Diwan"
                />
                <div class="d-flex flex-column">
                  <p class="text mb-1">Card Number</p>
                  <input
                    class="form-control mb-3"
                    type="text"
                    placeholder="1234 5678 123456"
                  />
                </div>
                <div class="d-flex flex-column">
                  <p class="text mb-1">Expiry</p>
                  <input
                    class="form-control mb-3"
                    type="text"
                    placeholder="MM/YYYY"
                  />
                </div>
                <div class="d-flex flex-column">
                  <p class="text mb-1">CVV/CVC</p>
                  <input
                    class="form-control mb-3 pt-2"
                    type="password"
                    placeholder="***"
                  />
                </div>
              </div>
              <div class="row">
                <p class="h8 py-3">Pay through UPI</p>
                <img src="http://127.0.0.1:5001/uploads/qr.png" alt="" />
              </div>
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="button button-blue">Pay</button>
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
</style>
