import type { DataProvider } from 'react-admin'
import api from '@/api/axios'

/** baseURL в axios уже задан как /api */
const apiPath = ''

/**
 * Data provider для react-admin, работающий с нашим REST API.
 * Ресурсы: users, roles.
 */
export const dataProvider: DataProvider = {
  getList: async (resource, params) => {
    const pagination = params.pagination ?? { page: 1, perPage: 10 }
    const { page, perPage } = pagination
    const skip = (page - 1) * perPage
    const url = `${apiPath}/${resource}?skip=${skip}&limit=${perPage}`
    const { data } = await api.get(url)
    const list = Array.isArray(data) ? data : []
    // Бэкенд не отдаёт total — запрашиваем ещё один раз с большим limit для total (или используем length)
    const total = list.length < perPage ? skip + list.length : 9999
    return { data: list, total }
  },

  getOne: async (resource, params) => {
    const { data } = await api.get(`${apiPath}/${resource}/${params.id}`)
    return { data }
  },

  getMany: async (resource, params) => {
    const promises = params.ids.map((id) =>
      api.get(`${apiPath}/${resource}/${id}`).then((r) => r.data)
    )
    const data = await Promise.all(promises)
    return { data }
  },

  getManyReference: async () => {
    return { data: [], total: 0 }
  },

  create: async (resource, params) => {
    const { data } = await api.post(`${apiPath}/${resource}`, params.data)
    return { data }
  },

  update: async (resource, params) => {
    const { data } = await api.patch(
      `${apiPath}/${resource}/${params.id}`,
      params.data
    )
    return { data }
  },

  updateMany: async () => {
    throw new Error('updateMany not implemented')
  },

  delete: async (resource, params) => {
    await api.delete(`${apiPath}/${resource}/${params.id}`)
    return {
      data: (params.previousData ?? { id: params.id }) as any,
    }
  },

  deleteMany: async () => {
    throw new Error('deleteMany not implemented')
  },
}
