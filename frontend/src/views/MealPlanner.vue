<template>
  <div class="px-4 py-8">
    <div class="max-w-4xl mx-auto">
      <h1 class="text-3xl font-bold text-gray-900 mb-8 text-center">
        🍽️ Personalized Meal Planner
      </h1>

      <!-- User Input Form -->
      <div class="card mb-8" v-if="!showResults">
        <h2 class="text-xl font-semibold mb-6">Tell us about yourself</h2>
        
        <form @submit.prevent="generateMealPlan" class="space-y-6">
          <div class="grid md:grid-cols-2 gap-6">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Age</label>
              <input 
                v-model.number="userProfile.age" 
                type="number" 
                required 
                min="1" 
                max="120"
                class="input-field"
                placeholder="Enter your age"
              >
            </div>
            
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Gender</label>
              <select v-model="userProfile.gender" required class="input-field">
                <option value="">Select gender</option>
                <option value="male">Male</option>
                <option value="female">Female</option>
              </select>
            </div>
            
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Height (cm)</label>
              <input 
                v-model.number="userProfile.height" 
                type="number" 
                required 
                min="100" 
                max="250"
                class="input-field"
                placeholder="Enter height in cm"
              >
            </div>
            
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Weight (kg)</label>
              <input 
                v-model.number="userProfile.weight" 
                type="number" 
                required 
                min="30" 
                max="300"
                class="input-field"
                placeholder="Enter weight in kg"
              >
            </div>
            
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Activity Level</label>
              <select v-model="userProfile.activity_level" required class="input-field">
                <option value="">Select activity level</option>
                <option value="sedentary">Sedentary (little/no exercise)</option>
                <option value="light">Light (light exercise 1-3 days/week)</option>
                <option value="moderate">Moderate (moderate exercise 3-5 days/week)</option>
                <option value="active">Active (hard exercise 6-7 days/week)</option>
                <option value="very_active">Very Active (very hard exercise, physical job)</option>
              </select>
            </div>
            
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Goal</label>
              <select v-model="userProfile.goal" required class="input-field">
                <option value="">Select your goal</option>
                <option value="weight_loss">Weight Loss</option>
                <option value="maintenance">Maintain Weight</option>
                <option value="weight_gain">Weight Gain</option>
              </select>
            </div>
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Dietary Preference</label>
            <select v-model="userProfile.dietary_preference" required class="input-field">
              <option value="">Select dietary preference</option>
              <option value="vegetarian">Vegetarian</option>
              <option value="non_vegetarian">Non-Vegetarian</option>
              <option value="mixed">Mixed Diet</option>
            </select>
          </div>
          
          <div class="text-center">
            <button 
              type="submit" 
              :disabled="loading"
              class="btn-primary text-lg px-8 py-3 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <span v-if="loading">🔄 Generating Plan...</span>
              <span v-else">🎯 Generate My Meal Plan</span>
            </button>
          </div>
        </form>
      </div>

      <!-- Results Section -->
      <div v-if="showResults && recommendations" class="space-y-8">
        <!-- BMR & Calories Info -->
        <div class="card bg-gradient-to-r from-primary-50 to-green-50">
          <div class="grid md:grid-cols-2 gap-6 text-center">
            <div>
              <h3 class="text-lg font-semibold text-gray-700 mb-2">Your BMR</h3>
              <p class="text-3xl font-bold text-primary-600">{{ recommendations.bmr }} kcal</p>
              <p class="text-sm text-gray-600">Basal Metabolic Rate</p>
            </div>
            <div>
              <h3 class="text-lg font-semibold text-gray-700 mb-2">Daily Calories</h3>
              <p class="text-3xl font-bold text-primary-600">{{ recommendations.daily_calories }} kcal</p>
              <p class="text-sm text-gray-600">Total daily requirement</p>
            </div>
          </div>
        </div>

        <!-- Meal Plans -->
        <div class="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
          <MealCard 
            title="🌅 Breakfast" 
            :foods="recommendations.breakfast"
            color="bg-yellow-50 border-yellow-200"
          />
          <MealCard 
            title="🌞 Lunch" 
            :foods="recommendations.lunch"
            color="bg-orange-50 border-orange-200"
          />
          <MealCard 
            title="🌙 Dinner" 
            :foods="recommendations.dinner"
            color="bg-blue-50 border-blue-200"
          />
          <MealCard 
            title="🍎 Snacks" 
            :foods="recommendations.snacks"
            color="bg-green-50 border-green-200"
          />
        </div>

        <!-- Action Buttons -->
        <div class="text-center space-x-4">
          <button 
            @click="generateMealPlan" 
            class="btn-primary"
          >
            🔄 Generate New Plan
          </button>
          <button @click="resetForm" class="btn-secondary">
            ✏️ Edit Profile
          </button>
        </div>
      </div>

      <!-- Error Message -->
      <div v-if="error" class="card bg-red-50 border-red-200 text-center">
        <div class="text-red-600">
          <h3 class="font-semibold mb-2">⚠️ Error</h3>
          <p>{{ error }}</p>
          <button @click="error = null" class="btn-secondary mt-4">Try Again</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, reactive } from 'vue'
import MealCard from '../components/MealCard.vue'
import { nutritionApi } from '../services/api'

export default {
  name: 'MealPlanner',
  components: {
    MealCard
  },
  setup() {
    const loading = ref(false)
    const showResults = ref(false)
    const error = ref(null)
    const recommendations = ref(null)
    
    const userProfile = reactive({
      age: null,
      height: null,
      weight: null,
      gender: '',
      activity_level: '',
      goal: '',
      dietary_preference: ''
    })

    const generateMealPlan = async () => {
      loading.value = true
      error.value = null
      
      try {
        const response = await nutritionApi.getRecommendations(userProfile)
        recommendations.value = response.data
        showResults.value = true
      } catch (err) {
        error.value = err.response?.data?.detail || 'Failed to generate meal plan. Please try again.'
        console.error('Error generating meal plan:', err)
      } finally {
        loading.value = false
      }
    }

    const generateNewPlan = () => {
      generateMealPlan()
    }

    const resetForm = () => {
      showResults.value = false
      recommendations.value = null
      error.value = null
    }

    return {
      userProfile,
      loading,
      showResults,
      error,
      recommendations,
      generateMealPlan,
      generateNewPlan,
      resetForm
    }
  }
}
</script>
