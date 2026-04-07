import { setActivePinia, createPinia } from 'pinia'
import { beforeEach, describe, expect, it, vi } from 'vitest'

describe('cartStore', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
  })

  it('starts with empty items and no coupon', async () => {
    const { useCartStore } = await import('../cartStore')
    const store = useCartStore()
    expect(store.items).toHaveLength(0)
    expect(store.coupon).toBeNull()
  })

  it('addItem appends an item', async () => {
    const { useCartStore } = await import('../cartStore')
    const store = useCartStore()
    store.addItem({ productName: 'ipad', qty: 1, unitPrice: 2399 })
    expect(store.items).toHaveLength(1)
    expect(store.items[0].productName).toBe('ipad')
  })

  it('removeItem removes by index', async () => {
    const { useCartStore } = await import('../cartStore')
    const store = useCartStore()
    store.addItem({ productName: 'ipad', qty: 1, unitPrice: 2399 })
    store.addItem({ productName: 'beer', qty: 12, unitPrice: 25 })
    store.removeItem(0)
    expect(store.items).toHaveLength(1)
    expect(store.items[0].productName).toBe('beer')
  })

  it('subtotal computes correctly without promotion', async () => {
    const { useCartStore } = await import('../cartStore')
    const store = useCartStore()
    store.addItem({ productName: 'ipad', qty: 2, unitPrice: 100 })
    expect(store.subtotal).toBe(200)
  })

  it('checkout calls fetch and returns order', async () => {
    const mockOrder = { id: 1, total_amount: 3083.60 }
    global.fetch = vi.fn().mockResolvedValueOnce({
      ok: true,
      json: async () => ({ success: true, data: mockOrder }),
    } as any)

    const { useCartStore } = await import('../cartStore')
    const store = useCartStore()
    store.addItem({ productName: 'ipad', qty: 1, unitPrice: 2399 })
    store.settledAt = '2015-11-11'

    const result = await store.checkout()
    expect(result.id).toBe(1)
    expect(fetch).toHaveBeenCalledWith('/api/checkouts', expect.objectContaining({ method: 'POST' }))
  })
})
