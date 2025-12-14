import { ApolloClient, InMemoryCache, createHttpLink, split } from '@apollo/client'
import { GraphQLWsLink } from '@apollo/client/link/subscriptions'
import { getMainDefinition } from '@apollo/client/utilities'
import { createClient } from 'graphql-ws'
import { onError } from '@apollo/client/link/error'
import { setContext } from '@apollo/client/link/context'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'
const WS_URL = import.meta.env.VITE_WS_URL || 'ws://localhost:8000'

// HTTP link for queries and mutations
const httpLink = createHttpLink({
  uri: `${API_URL}/graphql/`,
})

// WebSocket link for subscriptions
const wsLink = new GraphQLWsLink(
  createClient({
    url: `${WS_URL}/graphql/`,
    connectionParams: () => ({
      organizationSlug: localStorage.getItem('organizationSlug') || '',
    }),
  })
)

// Add organization header to all requests
const authLink = setContext((_, { headers }) => {
  const organizationSlug = localStorage.getItem('organizationSlug') || ''
  return {
    headers: {
      ...headers,
      'X-Organization-Slug': organizationSlug,
    },
  }
})

// Error handling link
const errorLink = onError(({ graphQLErrors, networkError }) => {
  if (graphQLErrors) {
    graphQLErrors.forEach(({ message, locations, path }) => {
      console.error(`[GraphQL error]: Message: ${message}, Location: ${locations}, Path: ${path}`)
    })
  }
  if (networkError) {
    console.error(`[Network error]: ${networkError}`)
  }
})

// Split link based on operation type
const splitLink = split(
  ({ query }) => {
    const definition = getMainDefinition(query)
    return definition.kind === 'OperationDefinition' && definition.operation === 'subscription'
  },
  wsLink,
  authLink.concat(httpLink)
)

export const apolloClient = new ApolloClient({
  link: errorLink.concat(splitLink),
  cache: new InMemoryCache({
    typePolicies: {
      Query: {
        fields: {
          projects: {
            merge(_existing, incoming) {
              return incoming
            },
          },
          tasks: {
            merge(_existing, incoming) {
              return incoming
            },
          },
        },
      },
    },
  }),
  defaultOptions: {
    watchQuery: {
      fetchPolicy: 'cache-and-network',
    },
  },
})
