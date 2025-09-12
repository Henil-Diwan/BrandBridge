import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import LoginView from '@/views/LoginView.vue'
import RegisterView from '@/views/RegisterView.vue'
import LogoutView from '@/views/LogoutView.vue'
import SponsorRegisterView from '@/views/SponsorRegisterView.vue'
import InfluencerRegisterView from '@/views/InfluencerRegisterView.vue'
import SponsorHomeView from '@/views/SponsorHomeView.vue'
import InfluencerHome from '@/views/InfluencerHome.vue'
import AdminHomeView from '@/views/AdminHomeView.vue'
import CreateCampaignView from '@/views/CreateCampaignView.vue'
import CreateRequestView from '@/views/CreateRequestView.vue'
import RateView from '@/views/RateView.vue'
import MyCampaignsView from '@/views/MyCampaignsView.vue'
import UpdateCampaignView from '@/views/UpdateCampaignView.vue'
import UpdateAdView from '@/views/UpdateAdView.vue'
import SponsorProfileView from '@/views/SponsorProfileView.vue'
import SponsorStatsView from '@/views/SponsorStatsView.vue'
import AllCampaignsView from '@/views/AllCampaignsView.vue'
import SavedCampaignsView from '@/views/SavedCampaignsView.vue'
import InfluencerStatsView from '@/views/InfluencerStatsView.vue'
import InfluencerProfileView from '@/views/InfluencerProfileView.vue'
import UpdateInfluencerView from '@/views/UpdateInfluencerView.vue'
import ChangeCampaignView from '@/views/ChangeCampaignView.vue'
import AdminCampaignView from '@/views/AdminCampaignView.vue'
import AdminSponsorView from '@/views/AdminSponsorView.vue'
import AdminInfluencerView from '@/views/AdminInfluencerView.vue'
import AdminFlaggedView from '@/views/AdminFlaggedView.vue'
import PublicInfluencerProfileView from '@/views/PublicInfluencerProfileView.vue'
import ShowCampaignView from '@/views/ShowCampaignView.vue'
import SearchView from '@/views/SearchView.vue'
import AdminRequestsView from '@/views/AdminRequestsView.vue'
import ChatView from '@/views/ChatView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/about',
      name: 'about',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/AboutView.vue')
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView
    },
    {
      path: '/register',
      name: 'register',
      component: RegisterView
    },
    {
      path: '/logout',
      name: 'logout',
      component: LogoutView
    },
    {
      path: '/sponsor_register/:creator',
      name: 'sponsor_register',
      component: SponsorRegisterView
    },
    {
      path: '/influencer_register/:creator',
      name: 'influencer_register',
      component: InfluencerRegisterView
    },
    {
      path: '/sponsorhome',
      name: 'sponsor_home',
      component: SponsorHomeView
    },
    {
      path: '/influencerhome',
      name: 'influencer_home',
      component: InfluencerHome
    },
    {
      path: '/adminhome',
      name: 'admin_home',
      component: AdminHomeView
    },
    {
      path: '/create',
      name: 'create_campaign',
      component: CreateCampaignView
    },
    {
      path: '/create_request/:campaign',
      name: 'create_request',
      component: CreateRequestView
    },
    {
      path: '/rate/:influencer',
      name: 'rate',
      component: RateView
    },
    {
      path: '/my_campaigns',
      name: 'my_campaigns',
      component: MyCampaignsView
    },
    {
      path: '/update/:campaign',
      name: 'update_campaign',
      component: UpdateCampaignView
    },
    {
      path: '/update_request/:ad',
      name: 'update_request',
      component: UpdateAdView
    },
    {
      path: '/sponsor_profile',
      name: 'sponsor_profile',
      component: SponsorProfileView
    },
    {
      path: '/sponsor_stats',
      name: 'sponsor_stats',
      component: SponsorStatsView
    },
    {
      path: '/all_campaigns',
      name: 'all_campaigns',
      component: AllCampaignsView
    },
    {
      path: '/saved_campaigns',
      name: 'saved_campaigns',
      component: SavedCampaignsView
    },
    {
      path: '/influencer_stats',
      name: 'influencer_stats',
      component: InfluencerStatsView
    },
    {
      path: '/influencer_profile',
      name: 'influencer_profile',
      component: InfluencerProfileView
    },
    {
      path: '/update_influencer',
      name: 'update_influencer',
      component: UpdateInfluencerView
    },
    {
      path: '/change_campaign/:campaign',
      name: 'change_campaign',
      component: ChangeCampaignView
    },
    {
      path: '/admin_campaigns',
      name: 'admin_campaigns',
      component: AdminCampaignView
    },
    {
      path: '/admin_sponsors',
      name: 'admin_sponsors',
      component: AdminSponsorView
    },
    {
      path: '/admin_influencers',
      name: 'admin_influencers',
      component: AdminInfluencerView
    },
    {
      path: '/admin_flagged',
      name: 'admin_flagged',
      component: AdminFlaggedView
    },
    {
      path: '/view_influencer/:influencer',
      name: 'view_influencer',
      component: PublicInfluencerProfileView
    },
    {
      path: '/show_campaign/:campaign',
      name: 'show_campaign',
      component: ShowCampaignView
    },
    {
      path: '/search',
      name: 'search',
      component: SearchView
    },
    {
      path: '/admin_requests',
      name: 'admin_requests',
      component: AdminRequestsView
    },
    {
      path: '/chat/:chatter1/:chatter2',
      name: 'chat',
      component: ChatView
    }
  ]
})

export default router
