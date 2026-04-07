import { setActivePinia, createPinia } from 'pinia'
import { beforeEach, describe, expect, it, vi } from 'vitest'

describe('orderStore', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
  })

  it('starts with empty orders', async () => {
    const { useOrderStore } = await import('../orderStore')
    const store = useOrderStore()
    expect(store.orders).toHaveLength(0)
    expect(store.pagination.total_elements).toBe(0)
  })

  it('fetchOrders populates orders and pagination', async () => {
    const mockData = {
      items: [{ id: 1, settled_at: '2015-11-11', total_amount: 3083.6, created_at: '' }],
      pagination: { page: 1, size: 20, total_elements: 1, total_pages: 1 },
    }
    global.fetch = vi.fn().mockResolvedValueOnce({
      ok: true,
      json: async () => ({ success: true, data: mockData }),
    } as any)

    const { useOrderStore } = await import('../orderStore')
    const store = useOrderStore()
    await store.fetchOrders()

    expect(store.orders).toHaveLength(1)
    expect(store.orders[0].id).toBe(1)
    expect(store.pagination.total_elements).toBe(1)
  })

  it('fetchOrderDetail returns order with items', async () => {
    const mockDetail = { id: 1, settled_at: '2015-11-11', total_amount: 3083.6, created_at: '', items: [], promotions: [], coupon: null }
    global.fetch = vi.fn().mockResolvedValueOnce({
      ok: true,
      json: async () => ({ success: true, data: mockDetail }),
    } as any)

    const { useOrderStore } = await import('../orderStore')
    const store = useOrderStore()
    const detail = await store.fetchOrderDetail(1)
    expect(detail.id).toBe(1)
  })
})
