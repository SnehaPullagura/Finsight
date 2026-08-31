with open("frontend/src/services/api.ts", "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace("export const api = {", """export const api = {
  get: (url: string, config?: any) => apiClient.get(url, config),
  post: (url: string, data?: any, config?: any) => apiClient.post(url, data, config),
  put: (url: string, data?: any, config?: any) => apiClient.put(url, data, config),
  delete: (url: string, config?: any) => apiClient.delete(url, config),""")

with open("frontend/src/services/api.ts", "w", encoding="utf-8") as f:
    f.write(content)

print("Added generic HTTP methods to api object.")
