import { computed, ref } from 'vue'
import { defineStore } from 'pinia'

export interface CartItem {
  productName: string
  qty: number
  unitPrice: number
}

export interface CartPromotion {
  date: string
  discountRate: number
  category: string
}

export interface CartCoupon {
  expiry: string
  threshold: number
  discount: number
}

export const useCartStore = defineStore('cart', () => {
  const items = ref<CartItem[]>([])
  const promotions = ref<CartPromotion[]>([])
  const coupon = ref<CartCoupon | null>(null)
  const settledAt = ref<string>(new Date().toISOString().slice(0, 10))

  const subtotal = computed(() =>
    items.value.reduce((sum, item) => sum + item.qty * item.unitPrice, 0),
  )

  function addItem(item: CartItem) {
    items.value.push({ ...item })
  }

  function removeItem(index: number) {
    items.value.splice(index, 1)
  }

  function addPromotion(promo: CartPromotion) {
    promotions.value.push({ ...promo })
  }

  function removePromotion(index: number) {
    promotions.value.splice(index, 1)
  }

  function setCoupon(c: CartCoupon | null) {
    coupon.value = c
  }

  function reset() {
    items.value = []
    promotions.value = []
    coupon.value = null
    settledAt.value = new Date().toISOString().slice(0, 10)
  }

  async function checkout(): Promise<any> {
    const payload = {
      settled_at: settledAt.value,
      items: items.value.map((i) => ({
        product_name: i.productName,
        qty: i.qty,
        unit_price: i.unitPrice,
      })),
      promotions: promotions.value.map((p) => ({
        date: p.date,
        discount_rate: p.discountRate,
        category: p.category,
      })),
      coupon: coupon.value
        ? {
            expiry: coupon.value.expiry,
            threshold: coupon.value.threshold,
            discount: coupon.value.discount,
          }
        : null,
    }

    const res = await fetch('/api/checkouts', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    })

    const data = await res.json()
    if (!res.ok) throw new Error(data?.error?.message ?? 'Checkout failed')
    return data.data
  }

  return {
    items,
    promotions,
    coupon,
    settledAt,
    subtotal,
    addItem,
    removeItem,
    addPromotion,
    removePromotion,
    setCoupon,
    reset,
    checkout,
  }
})
