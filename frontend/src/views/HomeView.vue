<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import { useRouter } from 'vue-router';

let router = useRouter();
let current_user = ref({
  'user_id': 0,
  'username': "",
  'email': "",
  'type': ""
});

onMounted(async () => {
  try {
    const token = JSON.parse(localStorage.getItem('user'))?.access_token;
    console.log(token);
    
    if (!token) {
      throw new Error('No token found');
    }
    
    const response = await axios.get('http://127.0.0.1:5001/protected', {
      headers: {
        'Authorization': `Bearer ${token}`,
      },
    });

    current_user.value = response.data.logged_in_as;
    console.log(response);
    
    if(current_user.value.type == "sponsor"){
      router.push('/sponsorhome');
    }
    else if(current_user.value.type == "influencer"){
      router.push('/influencerhome');
    }
    else{
      router.push('/adminhome');
    }
    

  } catch (err) {

    router.push('/login')
  }
});

</script>