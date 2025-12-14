import { useState, useEffect, useCallback } from 'react'
import { useQuery, useMutation } from '@apollo/client'
import { GET_PROJECTS } from '../graphql/queries'
import { CREATE_PROJECT } from '../graphql/mutations'
import { ProjectList, ProjectForm } from '../components/projects'
import { Button, Modal } from '../components/ui'
import { Project, CreateProjectInput } from '../types'

export default function Dashboard() {
  const [isModalOpen, setIsModalOpen] = useState(false)
  const [organizationSlug, setOrganizationSlug] = useState(
    () => localStorage.getItem('organizationSlug') || 'demo-org'
  )

  const { data, loading, error, refetch } = useQuery(GET_PROJECTS, {
    variables: { organizationSlug },
  })

  // Listen for organization changes from sidebar
  const handleOrgChange = useCallback((event: CustomEvent<string>) => {
    setOrganizationSlug(event.detail)
  }, [])

  useEffect(() => {
    window.addEventListener('organizationChanged', handleOrgChange as EventListener)
    return () => {
      window.removeEventListener('organizationChanged', handleOrgChange as EventListener)
    }
  }, [handleOrgChange])

  // Refetch when organization changes
  useEffect(() => {
    refetch({ organizationSlug })
  }, [organizationSlug, refetch])

  const [createProject, { loading: creating }] = useMutation(CREATE_PROJECT, {
    onCompleted: () => {
      setIsModalOpen(false)
      refetch()
    },
  })

  const handleCreateProject = (input: CreateProjectInput) => {
    createProject({
      variables: { input },
      optimisticResponse: {
        createProject: {
          __typename: 'ProjectPayload',
          project: {
            __typename: 'ProjectType',
            id: 'temp-id',
            name: input.name,
            description: input.description || '',
            status: input.status,
            dueDate: input.dueDate || null,
            createdAt: new Date().toISOString(),
            taskCount: 0,
            completedTasks: 0,
          },
          errors: [],
        },
      },
    })
  }

  const projects: Project[] = data?.projects || []

  return (
    <div>
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-xl font-semibold">Projects</h2>
        <Button onClick={() => setIsModalOpen(true)}>
          + New Project
        </Button>
      </div>

      <ProjectList 
        projects={projects} 
        loading={loading} 
        error={error?.message} 
      />

      <Modal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        title="Create New Project"
      >
        <ProjectForm
          onSubmit={handleCreateProject}
          onCancel={() => setIsModalOpen(false)}
          isLoading={creating}
          organizationSlug={organizationSlug}
        />
      </Modal>
    </div>
  )
}
