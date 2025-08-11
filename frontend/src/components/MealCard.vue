<template>
  <div class="card" :class="color">
    <h3 class="text-lg font-semibold mb-4 text-center">{{ title }}</h3>
    
    <div class="space-y-3">
      <div v-for="food in foods" :key="food.food_item" class="bg-white rounded-lg p-3 shadow-sm">
        <h4 class="font-medium text-gray-800 mb-2">{{ food.food_item }}</h4>
        
        <div class="grid grid-cols-2 gap-2 text-sm text-gray-600">
          <div>
            <span class="font-medium">Portion:</span> {{ food.portion_size }}g
          </div>
          <div>
            <span class="font-medium">Calories:</span> {{ food.calories }}
          </div>
          <div>
            <span class="font-medium">Protein:</span> {{ food.protein }}g
          </div>
          <div>
            <span class="font-medium">Carbs:</span> {{ food.carbs }}g
          </div>
          <div>
            <span class="font-medium">Fat:</span> {{ food.fat }}g
          </div>
          <div>
            <span class="inline-block px-2 py-1 text-xs rounded-full" 
                  :class="getCategoryColor(food.category)">
              {{ food.category }}
            </span>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Total Calories for this meal -->
    <div class="mt-4 pt-3 border-t border-gray-200">
      <div class="text-center">
        <span class="text-sm font-medium text-gray-700">Total: </span>
        <span class="text-lg font-bold text-primary-600">
          {{ totalCalories }} kcal
        </span>
      </div>
    </div>
  </div>
</template>

<script>
import { computed } from 'vue'

export default {
  name: 'MealCard',
  props: {
    title: {
      type: String,
      required: true
    },
    foods: {
      type: Array,
      required: true
    },
    color: {
      type: String,
      default: 'bg-gray-50 border-gray-200'
    }
  },
  setup(props) {
    const totalCalories = computed(() => {
      return props.foods.reduce((total, food) => total + (food.calories || 0), 0).toFixed(0)
    })

    const getCategoryColor = (category) => {
      const colors = {
        'Vegetarian': 'bg-green-100 text-green-800',
        'Non-Vegetarian': 'bg-red-100 text-red-800',
        'Mixed': 'bg-blue-100 text-blue-800'
      }
      return colors[category] || 'bg-gray-100 text-gray-800'
    }

    return {
      totalCalories,
      getCategoryColor
    }
  }
}
</script>
