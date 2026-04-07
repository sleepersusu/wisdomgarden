<template>
  <div class="orders-view">
    <h1>Order History</h1>

    <div v-if="orderStore.loading" class="loading">Loading…</div>

    <div v-else-if="orderStore.orders.length === 0" class="empty">
      No orders yet. <RouterLink to="/">Go checkout!</RouterLink>
    </div>

    <div v-else class="order-list">
      <div v-for="order in orderStore.orders" :key="order.id" class="card order-card">
        <div class="order-header" @click="toggleDetail(order.id)">
          <div class="order-meta">
            <span class="order-id">#{{ order.id }}</span>
            <span class="tag">{{ order.settled_at }}</span>
          </div>
          <div class="order-right">
            <span class="order-total">${{ order.total_amount.toFixed(2) }}</span>
            <ChevronDown :size="18" :class="['chevron', { open: expanded === order.id }]" />
          </div>
        </div>

        <div v-if="expanded === order.id && detail" class="order-detail">
          <div v-if="detail.promotions.length" class="detail-section">
            <span class="detail-label">Promotions</span>
            <div v-for="p in detail.promotions" :key="p.id" class="detail-row">
              {{ p.promo_date }} · {{ p.category }} · ×{{ p.discount_rate }}
            </div>
          </div>

          <div v-if="detail.coupon" class="detail-section">
            <span class="detail-label">Coupon</span>
            <div class="detail-row">
              Expires {{ detail.coupon.expiry }} · Min ${{ detail.coupon.threshold }} · -${{ detail.coupon.discount }}
            </div>
          </div>

          <div class="detail-section">
            <span class="detail-label">Items</span>
            <div v-for="item in detail.items" :key="item.id" class="detail-row item-row">
              <span>{{ item.product_key }} ×{{ item.qty }}</span>
              <span>@${{ item.unit_price.toFixed(2) }}</span>
              <span class="item-sub">${{ (item.qty * item.unit_price).toFixed(2) }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Pagination -->
    <div v-if="orderStore.pagination.total_pages > 1" class="pagination">
      <button
        class="btn-ghost"
        :disabled="orderStore.pagination.page <= 1"
        @click="changePage(orderStore.pagination.page - 1)"
      >Prev</button>
      <span>{{ orderStore.pagination.page }} / {{ orderStore.pagination.total_pages }}</span>
      <button
        class="btn-ghost"
        :disabled="orderStore.pagination.page >= orderStore.pagination.total_pages"
        @click="changePage(orderStore.pagination.page + 1)"
      >Next</button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { RouterLink } from 'vue-router'
import { ChevronDown } from 'lucide-vue-next'
import { useOrderStore } from '../stores/orderStore'
import type { OrderDetail } from '../stores/orderStore'

const orderStore = useOrderStore()
const expanded = ref<number | null>(null)
const detail = ref<OrderDetail | null>(null)

onMounted(() => orderStore.fetchOrders())

async function toggleDetail(orderId: number) {
  if (expanded.value === orderId) {
    expanded.value = null
    detail.value = null
    return
  }
  expanded.value = orderId
  detail.value = await orderStore.fetchOrderDetail(orderId)
}

function changePage(page: number) {
  orderStore.fetchOrders(page)
}
</script>

<style scoped>
.orders-view { display: flex; flex-direction: column; gap: 1.5rem; }
h1 { font-size: 1.8rem; margin-bottom: 0.5rem; }

.loading, .empty { color: var(--color-muted); text-align: center; padding: 2rem; }
.empty a { color: var(--color-primary); }

.order-list { display: flex; flex-direction: column; gap: 1rem; }

.order-card { padding: 1rem 1.5rem; }

.order-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  cursor: pointer;
}

.order-meta { display: flex; align-items: center; gap: 0.75rem; }
.order-id { font-family: 'Rubik', sans-serif; font-weight: 700; font-size: 1rem; color: var(--color-primary); }
.order-right { display: flex; align-items: center; gap: 0.75rem; }
.order-total { font-family: 'Rubik', sans-serif; font-weight: 700; font-size: 1.1rem; }

.chevron { transition: transform var(--transition); color: var(--color-muted); }
.chevron.open { transform: rotate(180deg); }

.order-detail {
  margin-top: 1rem;
  padding-top: 1rem;
  border-top: 1.5px solid var(--color-border);
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.detail-section { display: flex; flex-direction: column; gap: 0.4rem; }
.detail-label { font-size: 0.8rem; font-weight: 700; color: var(--color-muted); text-transform: uppercase; letter-spacing: 0.05em; }
.detail-row { font-size: 0.9rem; color: var(--color-text); padding: 0.2rem 0; }
.item-row { display: flex; gap: 1rem; }
.item-sub { margin-left: auto; font-weight: 600; color: var(--color-primary); }

.pagination { display: flex; align-items: center; justify-content: center; gap: 1rem; }
</style>
