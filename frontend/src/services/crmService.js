import { apiClient } from './authService'

class CRMService {
  // Contacts
  async getContacts() {
    return apiClient.get('/contacts')
  }

  async createContact(contactData) {
    return apiClient.post('/contacts', contactData)
  }

  async updateContact(id, contactData) {
    return apiClient.put(`/contacts/${id}`, contactData)
  }

  async deleteContact(id) {
    return apiClient.delete(`/contacts/${id}`)
  }

  // Companies
  async getCompanies() {
    return apiClient.get('/companies')
  }

  async createCompany(companyData) {
    return apiClient.post('/companies', companyData)
  }

  async updateCompany(id, companyData) {
    return apiClient.put(`/companies/${id}`, companyData)
  }

  async deleteCompany(id) {
    return apiClient.delete(`/companies/${id}`)
  }

  // Deals
  async getDeals() {
    return apiClient.get('/deals')
  }

  async createDeal(dealData) {
    return apiClient.post('/deals', dealData)
  }

  async updateDeal(id, dealData) {
    return apiClient.put(`/deals/${id}`, dealData)
  }

  async deleteDeal(id) {
    return apiClient.delete(`/deals/${id}`)
  }

  // Health check
  async healthCheck() {
    return apiClient.get('/health')
  }
}

export const crmService = new CRMService()