<script setup>
import { ref, onMounted } from "vue";
import axios from "axios";
import { useRouter } from "vue-router";
import SponsorHeader from "@/components/SponsorHeader.vue";
import { toast } from 'vue3-toastify';
import 'vue3-toastify/dist/index.css';

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
let campaigns = ref([]);
let taskId = ref("");

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

    const response2 = await axios.get(
      "http://127.0.0.1:5001/my_campaigns",
      {
        params: { user_id: current_user.value.user_id }, // Pass user_id as a query parameter
      }
    );

    console.log(response2);

    // Extract data from the response and assign it to the respective variables

    campaigns.value = response2.data.campaigns;
  } catch (err) {
    console.log(err);
    router.push("/login");
  }
});

let deleteCampaign = async (campaignId) => {
      try {

        const delete_response = await axios.delete(`http://127.0.0.1:5001/delete_campaign/${campaignId}`);

        toast("Campaign Deleted Successfully", {
                theme: "auto",
                type: "success",
                dangerouslyHTMLString: true,
                onClose: () => {
                    router.go();
                },
            autoClose: 1000
            });
        
      } catch (error) {
        toast("An Error Occured", {
                theme: "auto",
                type: "error",
                dangerouslyHTMLString: true,
                autoClose: 1000
            });
            console.log(error);
      }
    };

let downloadCSV = async () => {

    const response = await fetch(`http://127.0.0.1:5001/download_csv/${current_sponsor.value.id}`);
    const data = await response.json()
    if(response.ok){
        taskId.value = data["task_id"]
        const intv = setInterval(async () => {
          const csv_resp = await fetch(`http://127.0.0.1:5001/get_csv/${taskId.value}`);
          if(csv_resp.ok){
            clearInterval(intv);
            window.location.href = `http://127.0.0.1:5001/get_csv/${taskId.value}`
          }
        },100)
    }
}


</script>

<template>
  <main>
    <SponsorHeader />

    <h3 class="mt-5">Your Campaigns</h3>
    
    <button class="btn btn-primary my-3" @click="downloadCSV">Download CSV</button>

    <div v-if="campaigns.length > 0">
      <div class="row">
        <div class="col-lg-3" v-for="campaign in campaigns" :key="campaign.id">
          <div class="card" style="width: 18rem">
            <div class="card-body">
              <h5 class="card-title"><RouterLink to="/">{{ campaign.name }}</RouterLink></h5>
              <p class="card-text">
                {{ campaign.desc }}
              </p>
            </div>
            <ul class="list-group list-group-flush">
              <li class="list-group-item">
                Preferred Category: {{ campaign.category }}
              </li>
              <li class="list-group-item">Goals: {{ campaign.goals }}</li>
              <li class="list-group-item">Budget: {{ campaign.budget }}</li>
              <li class="list-group-item">Start: {{ campaign.start_date }}</li>
              <li class="list-group-item">End: {{ campaign.end_date }}</li>
              <li class="list-group-item">Views: {{ campaign.views }}</li>
            </ul>
              <div v-if="campaign.Status !== 'Accepted'" class="card-body text-center">
                  <router-link :to="'/update/' + campaign.id" class="btn btn-primary mx-2">Update</router-link>
                  <button @click="deleteCampaign(campaign.id)" class="btn btn-primary mx-2">Delete</button>
                </div>
            </div>
          </div>
        </div>
      </div>

    <div v-else>
      <p>No Campaigns Created</p>
    </div>
  </main>
</template>
