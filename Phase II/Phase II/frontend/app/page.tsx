"use client"

import { useEffect, useState } from "react"
import { useRouter } from "next/navigation"
import { authClient } from "@/lib/auth-client"
import { api, Task } from "@/lib/api"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card"
import { Navbar } from "@/components/Navbar"

export default function DashboardPage() {
  const router = useRouter()
  const { data: session, isPending } = authClient.useSession()
  const [tasks, setTasks] = useState<Task[]>([])
  const [newTaskTitle, setNewTaskTitle] = useState("")
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    if (!isPending && !session) {
      router.push("/auth")
    } else if (session) {
      loadTasks()
    }
  }, [session, isPending, router])

  const loadTasks = async () => {
    setLoading(true)
    try {
      const data = await api.getTasks()
      setTasks(data)
    } catch (error) {
      console.error("Failed to load tasks", error)
    } finally {
      setLoading(false)
    }
  }

  const handleCreateTask = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!newTaskTitle.trim()) return

    try {
      const task = await api.createTask({ title: newTaskTitle })
      setTasks([...tasks, task])
      setNewTaskTitle("")
    } catch (error) {
      console.error("Failed to create task", error)
    }
  }

  const handleToggleComplete = async (task: Task) => {
    try {
      const updated = await api.toggleTaskComplete(task.id)
      setTasks(tasks.map((t) => (t.id === task.id ? updated : t)))
    } catch (error) {
      console.error("Failed to update task", error)
    }
  }

  const handleDeleteTask = async (id: number) => {
    try {
      await api.deleteTask(id)
      setTasks(tasks.filter((t) => t.id !== id))
    } catch (error) {
      console.error("Failed to delete task", error)
    }
  }

  if (isPending || !session) {
    return <div className="flex min-h-screen items-center justify-center">Loading...</div>
  }

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
      <Navbar />
      <main className="container mx-auto p-4 md:p-6 lg:p-8">
        <div className="flex flex-col gap-6">
          <div className="flex flex-col gap-2">
            <h1 className="text-3xl font-bold tracking-tight">Tasks</h1>
            <p className="text-muted-foreground">Manage your daily tasks.</p>
          </div>

          <Card>
            <CardHeader>
              <CardTitle>Add New Task</CardTitle>
            </CardHeader>
            <CardContent>
              <form onSubmit={handleCreateTask} className="flex gap-2">
                <Input
                  placeholder="What needs to be done?"
                  value={newTaskTitle}
                  onChange={(e) => setNewTaskTitle(e.target.value)}
                />
                <Button type="submit">Add Task</Button>
              </form>
            </CardContent>
          </Card>

          <div className="grid gap-4">
            {loading ? (
              <div>Loading tasks...</div>
            ) : tasks.length === 0 ? (
              <div className="text-center text-muted-foreground py-8">No tasks found. Add a new task above!</div>
            ) : (
              tasks.map((task) => (
                <Card key={task.id} className="flex flex-row items-center justify-between p-4">
                  <div className="flex items-center gap-3">
                    <input
                      type="checkbox"
                      checked={task.completed}
                      onChange={() => handleToggleComplete(task)}
                      className="h-4 w-4 rounded border-gray-300 text-primary focus:ring-primary"
                    />
                    <span className={task.completed ? "line-through text-muted-foreground" : ""}>
                      {task.title}
                    </span>
                  </div>
                  <Button variant="ghost" size="sm" onClick={() => handleDeleteTask(task.id)}>
                    Delete
                  </Button>
                </Card>
              ))
            )}
          </div>
        </div>
      </main>
    </div>
  )
}
