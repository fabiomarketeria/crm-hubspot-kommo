import { useState, useEffect } from 'react'
import { crmService } from '../services/crmService'
import {
  UserGroupIcon,
  BuildingOfficeIcon,
  CurrencyDollarIcon,
  ChartBarIcon,
} from '@heroicons/react/24/outline'

const Dashboard = () => {
  const [stats, setStats] = useState({
    contacts: 0,
    companies: 0,
    deals: 0,
    totalDealsValue: 0
  })
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const [contactsRes, companiesRes, dealsRes] = await Promise.all([
          crmService.getContacts(),
          crmService.getCompanies(),
          crmService.getDeals()
        ])

        const deals = dealsRes.data
        const totalValue = deals.reduce((sum, deal) => sum + (deal.amount || 0), 0)

        setStats({
          contacts: contactsRes.data.length,
          companies: companiesRes.data.length,
          deals: deals.length,
          totalDealsValue: totalValue
        })
      } catch (error) {
        console.error('Error fetching stats:', error)
      } finally {
        setLoading(false)
      }
    }

    fetchStats()
  }, [])

  const statCards = [
    {
      name: 'Total Contacts',
      value: stats.contacts,
      icon: UserGroupIcon,
      color: 'text-blue-600',
      bgColor: 'bg-blue-100'
    },
    {
      name: 'Total Companies',
      value: stats.companies,
      icon: BuildingOfficeIcon,
      color: 'text-green-600',
      bgColor: 'bg-green-100'
    },
    {
      name: 'Active Deals',
      value: stats.deals,
      icon: CurrencyDollarIcon,
      color: 'text-purple-600',
      bgColor: 'bg-purple-100'
    },
    {
      name: 'Total Deal Value',
      value: `$${stats.totalDealsValue.toLocaleString()}`,
      icon: ChartBarIcon,
      color: 'text-yellow-600',
      bgColor: 'bg-yellow-100'
    }
  ]

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-gray-900">Dashboard</h1>
        <p className="mt-1 text-sm text-gray-600">
          Overview of your CRM data
        </p>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4">
        {statCards.map((stat) => (
          <div key={stat.name} className="card hover:shadow-lg transition-shadow duration-200">
            <div className="flex items-center">
              <div className={`flex-shrink-0 p-3 rounded-lg ${stat.bgColor}`}>
                <stat.icon className={`h-6 w-6 ${stat.color}`} />
              </div>
              <div className="ml-5 w-0 flex-1">
                <dl>
                  <dt className="text-sm font-medium text-gray-500 truncate">
                    {stat.name}
                  </dt>
                  <dd className="text-lg font-semibold text-gray-900">
                    {stat.value}
                  </dd>
                </dl>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Welcome Message */}
      <div className="card">
        <div className="text-center py-8">
          <ChartBarIcon className="mx-auto h-12 w-12 text-gray-400" />
          <h3 className="mt-2 text-sm font-medium text-gray-900">Welcome to CRM System</h3>
          <p className="mt-1 text-sm text-gray-500">
            Manage your contacts, companies, and deals in one place with HubSpot and Kommo integration.
          </p>
        </div>
      </div>
    </div>
  )
}

export default Dashboard