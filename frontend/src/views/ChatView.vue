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
let messages = ref([]);
let person1 = ref("");
let person2 = ref("");
let id = ref(0);
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
    if (current_user.value.type == "influencer") {
      current_influencer.value = response.data.current_influencer;
      id.value = current_influencer.value.id;
    } else if (current_user.value.type == "sponsor") {
      current_sponsor.value = response.data.current_sponsor;
      id.value = current_sponsor.value.id;
    }

    const response2 = await axios.get(`http://127.0.0.1:5001/chat/${route.params.chatter1}/${route.params.chatter2}`, {
    });

    console.log(response2);

    // Extract data from the response and assign it to the respective variables

    messages.value = response2.data.messages;
    person1.value = response2.data.person1_name;
    person2.value = response2.data.person2_name;

    
  } catch (err) {
    router.push("/login");
  }
});


const sendMessage = async () => {
  try {

    console.log(route.params.chatter1 == current_user.value.user_id ? route.params.chatter2 : route.params.chatter1);
    

    const messageData = {
      sender_id: current_user.value.user_id, 
      receiver_id: route.params.chatter1 == current_user.value.user_id ? route.params.chatter2 : route.params.chatter1,
      message: message.value,
      sender_type: current_user.value.type,
      receiver_type: "" // Adjust as per your logic
    };

    const response_send = await axios.post(
      `http://127.0.0.1:5001/send_message`,
      messageData
    );
    toast("Messgae Sent!", {
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
  <div v-if="current_user.type == 'influencer'">
    <InfluencerHeader />
  </div>
  <div v-else-if="current_user.type == 'sponsor'">
    <SponsorHeader />
  </div>
  <div v-else>
    <AdminHeader />
  </div>

  <h1>Chat between {{ person1 }} and {{ person2 }}</h1>
    <div v-if="messages.length > 0" class="chat-box">
      <div v-for="msg in messages" :key="msg.timestamp" class="message">
        <div class="sender">{{ msg.sender_name }}</div>
        <div class="message-text">{{ msg.message }}</div>
        <div class="timestamp">{{ msg.timestamp }}</div>
      </div>
    </div>
    <div v-else>
        No Chat Messages
    </div>

    <div class="my-5"> 

    <input type="text" v-model="message" placeholder="Type your message..." rows="3" class="message-input"></input>
    <br>
    <button @click="sendMessage" class="btn btn-primary">Send</button>
</div>

    <br />
</template>
