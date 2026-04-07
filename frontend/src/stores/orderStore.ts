import { ref } from 'vue'
import { defineStore } from 'pinia'

export interface OrderSummary {
  id: number
  settled_at: string
  total_amount: number
  created_at: string
}

export interface OrderDetail extends OrderSummary {
  items: { id: number; product_key: string; qty: number; unit_price: number }[]
  promotions: { id: number; promo_date: string; discount_rate: number; category: string }[]
  coupon: { expiry: string; threshold: number; discount: number } | null
}

export interface Pagination {
  page: number
  size: number
  total_elements: number
  total_pages: number
}

export const useOrderStore = defineStore('orders', () => {
  const orders = ref<OrderSummary[]>([])
  const pagination = ref<Pagination>({ page: 1, size: 20, total_elements: 0, total_pages: 1 })
  const loading = ref(false)

  async function fetchOrders(page = 1, size = 20) {
    loading.value = true
    try {
      const res = await fetch(`/api/orders?page=${page}&size=${size}`)
      const data = await res.json()
      if (!res.ok) throw new Error(data?.error?.message ?? 'Failed to fetch orders')
      orders.value = data.data.items
      pagination.value = data.data.pagination
    } finally {
      loading.value = false
    }
  }

  async function fetchOrderDetail(orderId: number): Promise<OrderDetail> {
    const res = await fetch(`/api/orders/${orderId}`)
    const data = await res.json()
    if (!res.ok) throw new Error(data?.error?.message ?? 'Order not found')
    return data.data
  }

  return { orders, pagination, loading, fetchOrders, fetchOrderDetail }
})
