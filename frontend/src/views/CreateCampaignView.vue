<script setup>

import { ref, onMounted } from "vue";
import axios from "axios";
import { useRouter } from "vue-router";
import { toast } from 'vue3-toastify';
import 'vue3-toastify/dist/index.css';

let name = ref("");
let desc = ref("");
let category = ref("");
let start = ref("");
let end = ref("");
let budget = ref(0);
let goals = ref("");
let visibility = ref("")

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
    } catch (err) {
        router.push("/login");
    }
});

let goBack = () => {
    router.go(-1);
};

const createCampaign = async () => {
    const campaignData = {
        Name: name.value,
        Desc: desc.value,
        Category: category.value,
        Start: start.value,
        End: end.value,
        Budget: budget.value,
        Goals: goals.value,
        Visi: visibility.value,
        Created_by: current_sponsor.value.id
    };

    try {
        const response2 = await axios.post(
            "http://127.0.0.1:5001/create_campaign",
            campaignData,
            {
                headers: {
                    Authorization: `Bearer ${localStorage.getItem("user")?.access_token}`,
                },
            }
        );
        
        toast("Campaign Created Successfully", {
          theme: "auto",
          type: "success",
          dangerouslyHTMLString: true,
          onClose: () => {
            router.push(`/create_request/${response2.data.Campaign_ID}`);
          },
          autoClose: 1000
        });

        
    } catch (err) {
        console.log(err);
        toast("An Error Occured", {
          theme: "auto",
          type: "error",
          dangerouslyHTMLString: true,
          autoClose: 1000
        });
    }
};

</script>

<template>

  <h1>Create Campaign</h1>

    <form @submit.prevent="createCampaign">
  <div class="mb-3">
    <label for="exampleInputUsername1" class="form-label">Name</label>
    <input v-model="name" type="text" class="form-control" id="exampleInputUsername1" aria-describedby="usernamelHelp">
  </div>
  <div class="mb-3">
    <label for="exampleInputEmail1" class="form-label">Description</label>
    <input v-model="desc" type="text" class="form-control" id="exampleInputEmail1" aria-describedby="emailHelp">
  </div>
  <div class="mb-3">
    <label for="exampleInputType1" class="form-label">Category</label>
    <select v-model="category" class="form-select" aria-label="exampleInputType1">
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
    <label for="exampleInputEmail1" class="form-label">Start</label>
    <input v-model="start" type="datetime-local" class="form-control" id="exampleInputEmail1" aria-describedby="emailHelp">
  </div>
  <div class="mb-3">
    <label for="exampleInputEmail1" class="form-label">End</label>
    <input v-model="end" type="datetime-local" class="form-control" id="exampleInputEmail1" aria-describedby="emailHelp">
  </div>
  <div class="mb-3">
    <label for="exampleInputEmail1" class="form-label">Budget</label>
    <input v-model="budget" type="number" class="form-control" id="exampleInputEmail1" aria-describedby="emailHelp">
  </div>
  <div class="mb-3">
    <label for="exampleInputEmail1" class="form-label">Goals</label>
    <input v-model="goals" type="text" class="form-control" id="exampleInputEmail1" aria-describedby="emailHelp">
  </div>
  <div class="mb-3">
    <label for="exampleInputType1" class="form-label">Visibility</label>
    <select v-model="visibility" class="form-select" aria-label="exampleInputType1">
        <option value="" disabled selected>Default</option>
        <option value="All">Public</option>
        <option value="None">Private</option>
    </select>
  </div>
  <button type="submit" class="btn btn-primary">Submit</button>
</form>
<br>
<button @click="goBack">Back</button>
</template>