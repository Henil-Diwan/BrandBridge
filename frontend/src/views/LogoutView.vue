<script setup>
    import { useRouter } from 'vue-router';
    const router = useRouter();
    localStorage.removeItem('user');
    router.push('/login')
</script>