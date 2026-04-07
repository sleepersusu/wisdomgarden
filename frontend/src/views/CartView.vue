<template>
  <div class="cart-view">
    <h1>Shopping Cart</h1>

    <!-- Settlement Date -->
    <section class="card section">
      <label class="label" for="settled-at">Settlement Date</label>
      <input id="settled-at" type="date" v-model="cart.settledAt" style="max-width:200px" />
    </section>

    <!-- Items -->
    <section class="card section">
      <h2>Items</h2>
      <div v-for="(item, i) in cart.items" :key="i" class="row">
        <select v-model="item.productName" style="flex:2">
          <option value="" disabled>Select product</option>
          <option v-for="p in catalog" :key="p.key" :value="p.key">
            {{ p.display_name }} ({{ p.category }})
          </option>
        </select>
        <input type="number" v-model.number="item.qty" min="1" placeholder="Qty" style="flex:1" />
        <input type="number" v-model.number="item.unitPrice" min="0" step="0.01" placeholder="Unit price" style="flex:2" />
        <button class="btn-danger" @click="cart.removeItem(i)">
          <Trash2 :size="14" />
        </button>
      </div>
      <button class="btn-ghost mt" @click="cart.addItem({ productName: '', qty: 1, unitPrice: 0 })">
        <Plus :size="16" /> Add Item
      </button>
    </section>

    <!-- Promotions -->
    <section class="card section">
      <h2>Promotions</h2>
      <div v-for="(promo, i) in cart.promotions" :key="i" class="row">
        <input type="date" v-model="promo.date" style="flex:2" />
        <input type="number" v-model.number="promo.discountRate" min="0" max="1" step="0.01" placeholder="Rate (e.g. 0.7)" style="flex:1" />
        <select v-model="promo.category" style="flex:2">
          <option value="" disabled>Category</option>
          <option value="電子">電子 (Electronics)</option>
          <option value="食品">食品 (Food)</option>
          <option value="日用品">日用品 (Daily)</option>
          <option value="酒類">酒類 (Alcohol)</option>
        </select>
        <button class="btn-danger" @click="cart.removePromotion(i)">
          <Trash2 :size="14" />
        </button>
      </div>
      <button class="btn-ghost mt" @click="cart.addPromotion({ date: cart.settledAt, discountRate: 0.7, category: '電子' })">
        <Plus :size="16" /> Add Promotion
      </button>
    </section>

    <!-- Coupon -->
    <section class="card section">
      <h2>Coupon <span class="tag">optional</span></h2>
      <div v-if="cart.coupon" class="row">
        <input type="date" v-model="cart.coupon.expiry" placeholder="Expiry" style="flex:2" />
        <input type="number" v-model.number="cart.coupon.threshold" min="0" placeholder="Min amount" style="flex:1" />
        <input type="number" v-model.number="cart.coupon.discount" min="0" placeholder="Discount" style="flex:1" />
        <button class="btn-danger" @click="cart.setCoupon(null)">
          <Trash2 :size="14" />
        </button>
      </div>
      <button v-else class="btn-ghost mt" @click="cart.setCoupon({ expiry: '', threshold: 1000, discount: 200 })">
        <Plus :size="16" /> Add Coupon
      </button>
    </section>

    <!-- Summary -->
    <section class="card section summary">
      <div class="summary-row">
        <span class="summary-label">Subtotal (no discount)</span>
        <span class="summary-amount">${{ cart.subtotal.toFixed(2) }}</span>
      </div>
      <div v-if="errorMsg" class="error-msg">{{ errorMsg }}</div>
      <div v-if="lastTotal !== null" class="result-row">
        <CheckCircle :size="20" class="check-icon" />
        <span>Total charged: <strong>${{ lastTotal.toFixed(2) }}</strong></span>
      </div>
      <button class="btn-cta" :disabled="isLoading || cart.items.length === 0" @click="doCheckout">
        <span v-if="isLoading">Processing…</span>
        <span v-else>Checkout</span>
      </button>
    </section>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { Plus, Trash2, CheckCircle } from 'lucide-vue-next'
import { useCartStore } from '../stores/cartStore'

const cart = useCartStore()
const catalog = ref<{ key: string; display_name: string; category: string }[]>([])
const isLoading = ref(false)
const errorMsg = ref('')
const lastTotal = ref<number | null>(null)

onMounted(async () => {
  const res = await fetch('/api/catalog')
  const data = await res.json()
  if (data.success) catalog.value = data.data
})

async function doCheckout() {
  errorMsg.value = ''
  lastTotal.value = null
  isLoading.value = true
  try {
    const order = await cart.checkout()
    lastTotal.value = order.total_amount
    cart.reset()
  } catch (e: any) {
    errorMsg.value = e.message ?? 'Checkout failed'
  } finally {
    isLoading.value = false
  }
}
</script>

<style scoped>
.cart-view { display: flex; flex-direction: column; gap: 1.5rem; }
h1 { font-size: 1.8rem; margin-bottom: 0.5rem; }
h2 { font-size: 1.1rem; margin-bottom: 1rem; }

.section { display: flex; flex-direction: column; gap: 0.75rem; }

.row {
  display: flex;
  gap: 0.5rem;
  align-items: center;
  flex-wrap: wrap;
}

.mt { margin-top: 0.25rem; }

.summary {
  background: linear-gradient(135deg, #f0fdff, #ecfeff);
  display: flex;
  flex-direction: column;
  gap: 1rem;
  align-items: flex-start;
}

.summary-row {
  display: flex;
  justify-content: space-between;
  width: 100%;
  font-size: 1rem;
}

.summary-label { color: var(--color-muted); }
.summary-amount { font-weight: 700; font-size: 1.2rem; color: var(--color-primary); }

.result-row {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 1.1rem;
  color: #166534;
}

.check-icon { color: var(--color-cta); }
.error-msg { color: #dc2626; font-size: 0.9rem; }
</style>
