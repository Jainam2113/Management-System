import { Link, useLocation } from 'react-router-dom'
import { useState, useEffect } from 'react'
import { useQuery, useMutation } from '@apollo/client'
import { GET_ORGANIZATIONS } from '../../graphql/queries'
import { CREATE_ORGANIZATION } from '../../graphql/mutations'

interface Organization {
  id: string
  name: string
  slug: string
  contactEmail: string
}

export default function Sidebar() {
  const location = useLocation()
  const [orgSlug, setOrgSlug] = useState(() => localStorage.getItem('organizationSlug') || 'demo-org')
  const [showOrgForm, setShowOrgForm] = useState(false)
  const [newOrg, setNewOrg] = useState({ name: '', slug: '', contactEmail: '' })
  const [formError, setFormError] = useState('')

  const { data, refetch } = useQuery(GET_ORGANIZATIONS)
  const organizations: Organization[] = data?.organizations || []

  const [createOrganization, { loading: creating }] = useMutation(CREATE_ORGANIZATION, {
    onCompleted: (data) => {
      if (data.createOrganization.errors?.length > 0) {
        setFormError(data.createOrganization.errors[0].message)
      } else {
        setOrgSlug(data.createOrganization.organization.slug)
        setShowOrgForm(false)
        setNewOrg({ name: '', slug: '', contactEmail: '' })
        setFormError('')
        refetch()
      }
    },
    onError: (error) => {
      setFormError(error.message)
    }
  })

  useEffect(() => {
    localStorage.setItem('organizationSlug', orgSlug)
    // Dispatch custom event to notify other components
    window.dispatchEvent(new CustomEvent('organizationChanged', { detail: orgSlug }))
  }, [orgSlug])

  const handleCreateOrg = (e: React.FormEvent) => {
    e.preventDefault()
    setFormError('')
    createOrganization({
      variables: {
        input: {
          name: newOrg.name,
          slug: newOrg.slug.toLowerCase().replace(/\s+/g, '-'),
          contactEmail: newOrg.contactEmail
        }
      }
    })
  }

  const navItems = [
    { path: '/', label: 'Dashboard', icon: '📊' },
  ]

  return (
    <aside className="w-64 border-r border-light-border dark:border-dark-border bg-white dark:bg-dark-bg-secondary flex flex-col">
      <div className="p-4 border-b border-light-border dark:border-dark-border">
        <label className="block text-xs text-light-text-secondary dark:text-dark-text-secondary mb-1">
          Organization
        </label>
        <select
          value={orgSlug}
          onChange={(e) => setOrgSlug(e.target.value)}
          className="input text-sm mb-2"
        >
          {organizations.map((org) => (
            <option key={org.id} value={org.slug}>{org.name}</option>
          ))}
        </select>
        
        <button
          onClick={() => setShowOrgForm(!showOrgForm)}
          className="w-full text-xs text-primary hover:text-primary-dark transition-colors flex items-center justify-center gap-1 py-1"
        >
          {showOrgForm ? '− Cancel' : '+ Add Organization'}
        </button>

        {showOrgForm && (
          <form onSubmit={handleCreateOrg} className="mt-3 space-y-2 animate-slideDown">
            <input
              type="text"
              placeholder="Organization Name"
              value={newOrg.name}
              onChange={(e) => setNewOrg({ ...newOrg, name: e.target.value, slug: e.target.value.toLowerCase().replace(/\s+/g, '-') })}
              className="input text-xs"
              required
            />
            <input
              type="text"
              placeholder="Slug (auto-generated)"
              value={newOrg.slug}
              onChange={(e) => setNewOrg({ ...newOrg, slug: e.target.value })}
              className="input text-xs"
              required
            />
            <input
              type="email"
              placeholder="Contact Email"
              value={newOrg.contactEmail}
              onChange={(e) => setNewOrg({ ...newOrg, contactEmail: e.target.value })}
              className="input text-xs"
              required
            />
            {formError && (
              <p className="text-xs text-red-500">{formError}</p>
            )}
            <button
              type="submit"
              disabled={creating}
              className="w-full btn btn-primary btn-sm"
            >
              {creating ? 'Creating...' : 'Create'}
            </button>
          </form>
        )}
      </div>
      <nav className="flex-1 p-4">
        <ul className="space-y-1">
          {navItems.map((item) => (
            <li key={item.path}>
              <Link
                to={item.path}
                className={`flex items-center gap-3 px-3 py-2 rounded-md text-sm transition-all duration-200 hover:scale-[1.02] ${
                  location.pathname === item.path
                    ? 'bg-primary/10 text-primary shadow-sm'
                    : 'hover:bg-light-bg-secondary dark:hover:bg-dark-bg'
                }`}
              >
                <span>{item.icon}</span>
                <span>{item.label}</span>
              </Link>
            </li>
          ))}
        </ul>
      </nav>
    </aside>
  )
}
