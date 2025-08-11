<template>
  <div class="px-4 py-8">
    <!-- Hero Section -->
    <div class="text-center mb-12">
      <h1 class="text-4xl md:text-6xl font-bold text-gray-900 mb-4">
        Welcome to <span class="text-primary-600">NutriWise</span>
      </h1>
      <p class="text-xl text-gray-600 mb-8 max-w-3xl mx-auto">
        Your AI-powered meal planning companion. Get personalized nutrition recommendations 
        based on your goals, preferences, and lifestyle.
      </p>
      <router-link to="/planner" class="btn-primary text-lg px-8 py-3 inline-block">
        Start Planning Your Meals
      </router-link>
    </div>

    <!-- Features Grid -->
    <div class="grid md:grid-cols-3 gap-8 mb-12">
      <div class="card text-center">
        <div class="text-4xl mb-4">🎯</div>
        <h3 class="text-xl font-semibold mb-2">Personalized Goals</h3>
        <p class="text-gray-600">
          Whether you want to lose weight, gain muscle, or maintain health, 
          we create plans tailored to your specific goals.
        </p>
      </div>
      
      <div class="card text-center">
        <div class="text-4xl mb-4">🧠</div>
        <h3 class="text-xl font-semibold mb-2">AI-Powered</h3>
        <p class="text-gray-600">
          Advanced machine learning algorithms analyze your profile to recommend 
          the perfect balance of nutrients for your lifestyle.
        </p>
      </div>
      
      <div class="card text-center">
        <div class="text-4xl mb-4">🌱</div>
        <h3 class="text-xl font-semibold mb-2">Dietary Preferences</h3>
        <p class="text-gray-600">
          Support for vegetarian, vegan, and mixed diets with authentic 
          Indian cuisine recommendations.
        </p>
      </div>
    </div>

    <!-- Stats Section -->
    <div class="bg-white rounded-2xl shadow-lg p-8 mb-12">
      <div class="grid md:grid-cols-4 gap-8 text-center">
        <div>
          <div class="text-3xl font-bold text-primary-600 mb-2">500+</div>
          <div class="text-gray-600">Food Items</div>
        </div>
        <div>
          <div class="text-3xl font-bold text-primary-600 mb-2">AI</div>
          <div class="text-gray-600">Powered</div>
        </div>
        <div>
          <div class="text-3xl font-bold text-primary-600 mb-2">24/7</div>
          <div class="text-gray-600">Available</div>
        </div>
        <div>
          <div class="text-3xl font-bold text-primary-600 mb-2">Free</div>
          <div class="text-gray-600">To Use</div>
        </div>
      </div>
    </div>

    <!-- How It Works -->
    <div class="text-center mb-12">
      <h2 class="text-3xl font-bold text-gray-900 mb-8">How It Works</h2>
      <div class="grid md:grid-cols-3 gap-8">
        <div class="flex flex-col items-center">
          <div class="w-16 h-16 bg-primary-100 rounded-full flex items-center justify-center mb-4">
            <span class="text-2xl font-bold text-primary-600">1</span>
          </div>
          <h3 class="text-lg font-semibold mb-2">Enter Your Details</h3>
          <p class="text-gray-600">Tell us about your age, weight, height, and fitness goals</p>
        </div>
        
        <div class="flex flex-col items-center">
          <div class="w-16 h-16 bg-primary-100 rounded-full flex items-center justify-center mb-4">
            <span class="text-2xl font-bold text-primary-600">2</span>
          </div>
          <h3 class="text-lg font-semibold mb-2">AI Analysis</h3>
          <p class="text-gray-600">Our ML model calculates your BMR and nutritional needs</p>
        </div>
        
        <div class="flex flex-col items-center">
          <div class="w-16 h-16 bg-primary-100 rounded-full flex items-center justify-center mb-4">
            <span class="text-2xl font-bold text-primary-600">3</span>
          </div>
          <h3 class="text-lg font-semibold mb-2">Get Recommendations</h3>
          <p class="text-gray-600">Receive personalized meal plans with exact portions</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Home'
}
</script>
