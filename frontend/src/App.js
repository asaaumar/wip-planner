import React, { useState, useEffect } from 'react';
import './App.css';

const API_BASE_URL = 'http://localhost:8000';

function Modal({ isOpen, onClose, children }) {
  if (!isOpen) return null;

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        {children}
      </div>
    </div>
  );
}

function EditTaskModal({ task, isOpen, onClose, onSave, onDelete }) {
  const [title, setTitle] = useState(task?.title || '');
  const [description, setDescription] = useState(task?.description || '');

  useEffect(() => {
    if (task) {
      setTitle(task.title);
      setDescription(task.description || '');
    }
  }, [task]);

  const handleSave = () => {
    onSave(task.id, { title, description });
    onClose();
  };

  const handleDelete = () => {
    onClose();
    onDelete(task);
  };

  return (
    <Modal isOpen={isOpen} onClose={onClose}>
      <div className="modal-header">Edit Task</div>
      <div className="modal-body">
        <label className="form-label">Title</label>
        <input
          type="text"
          className="form-input"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          placeholder="Task title"
        />
        
        <label className="form-label">Description</label>
        <textarea
          className="form-textarea"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          placeholder="Develop the initial prototype"
          rows="4"
        />
      </div>
      <div className="modal-footer">
        <button className="btn-primary" onClick={handleSave}>Save</button>
        <button className="btn-danger" onClick={handleDelete}>Delete</button>
      </div>
    </Modal>
  );
}

function DeleteTaskModal({ task, isOpen, onClose, onConfirm }) {
  return (
    <Modal isOpen={isOpen} onClose={onClose}>
      <div className="modal-header">Delete Task</div>
      <div className="modal-body">
        <p>Are you sure you want to delete this task?</p>
      </div>
      <div className="modal-footer">
        <button className="btn-danger" onClick={() => { onConfirm(task.id); onClose(); }}>
          Yes, Delete
        </button>
        <button className="btn-secondary" onClick={onClose}>No, Cancel</button>
      </div>
    </Modal>
  );
}

function NewTaskModal({ isOpen, onClose, onCreate }) {
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');

  const handleCreate = () => {
    if (title.trim()) {
      onCreate({ title, description });
      setTitle('');
      setDescription('');
      onClose();
    }
  };

  return (
    <Modal isOpen={isOpen} onClose={onClose}>
      <div className="modal-header">New Task</div>
      <div className="modal-body">
        <label className="form-label">Title</label>
        <input
          type="text"
          className="form-input"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          placeholder="Task title"
        />
        
        <label className="form-label">Description</label>
        <textarea
          className="form-textarea"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          placeholder="Task description (optional)"
          rows="4"
        />
      </div>
      <div className="modal-footer">
        <button className="btn-primary" onClick={handleCreate}>Create</button>
        <button className="btn-secondary" onClick={onClose}>Cancel</button>
      </div>
    </Modal>
  );
}

function SettingsModal({ isOpen, onClose, wipLimit, onSave }) {
  const [limit, setLimit] = useState(wipLimit);

  const handleSave = () => {
    onSave(limit);
    onClose();
  };

  return (
    <Modal isOpen={isOpen} onClose={onClose}>
      <div className="modal-header">Settings</div>
      <div className="modal-body">
        <label className="form-label">Work-In-Progress Limit</label>
        <input
          type="number"
          className="form-input"
          value={limit}
          onChange={(e) => setLimit(parseInt(e.target.value) || 1)}
          min="1"
        />
        <p className="form-help-text">
          Set the maximum number of tasks allowed in the "In Progress" column.
        </p>
      </div>
      <div className="modal-footer">
        <button className="btn-primary" onClick={handleSave}>Save Settings</button>
        <button className="btn-secondary" onClick={onClose}>Close</button>
      </div>
    </Modal>
  );
}

function TaskCard({ task, onMoveLeft, onMoveRight, onEdit, onDelete }) {
  const canMoveLeft = task.status !== 'todo';
  const canMoveRight = task.status !== 'done';
  const isDone = task.status === 'done';

  return (
    <div className="task-card">
      <div className="task-title">{task.title}</div>
      {task.description && <div className="task-description">{task.description}</div>}
      
      {!isDone && (
        <div className="task-actions">
          {canMoveLeft && (
            <button className="btn-move" onClick={() => onMoveLeft(task)}>
              Move ←
            </button>
          )}
          {canMoveRight && (
            <button className="btn-move" onClick={() => onMoveRight(task)}>
              Move →
            </button>
          )}
          <button className="btn-move" onClick={() => onEdit(task)}>
            Edit
          </button>
        </div>
      )}
    </div>
  );
}

function Column({ title, tasks, wipLimit, onMoveLeft, onMoveRight, onEdit, onDelete }) {
  const showWipLimit = title === 'In Progress' && wipLimit !== undefined;
  
  return (
    <div className="column">
      <div className="column-header">
        <h2>{title}</h2>
        {showWipLimit && <span className="wip-limit">(WIP limit: {wipLimit})</span>}
      </div>
      <div className="column-content">
        {tasks.length === 0 ? (
          <div className="empty-state">No tasks yet</div>
        ) : (
          tasks.map(task => (
            <TaskCard
              key={task.id}
              task={task}
              onMoveLeft={onMoveLeft}
              onMoveRight={onMoveRight}
              onEdit={onEdit}
              onDelete={onDelete}
            />
          ))
        )}
      </div>
    </div>
  );
}

function App() {
  const [tasks, setTasks] = useState([]);
  const [wipLimit, setWipLimit] = useState(1);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  
  // Modal states
  const [editModalOpen, setEditModalOpen] = useState(false);
  const [deleteModalOpen, setDeleteModalOpen] = useState(false);
  const [newTaskModalOpen, setNewTaskModalOpen] = useState(false);
  const [settingsModalOpen, setSettingsModalOpen] = useState(false);
  const [selectedTask, setSelectedTask] = useState(null);

  // Fetch tasks from API
  const fetchTasks = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/tasks/`);
      if (!response.ok) throw new Error('Failed to fetch tasks');
      const data = await response.json();
      setTasks(data);
      setError(null);
    } catch (err) {
      setError(err.message);
      console.error('Error fetching tasks:', err);
    } finally {
      setLoading(false);
    }
  };

  // Fetch settings (WIP limit)
  const fetchSettings = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/settings/`);
      if (!response.ok) throw new Error('Failed to fetch settings');
      const data = await response.json();
      setWipLimit(data.wip_limit);
    } catch (err) {
      console.error('Error fetching settings:', err);
    }
  };

  useEffect(() => {
    fetchTasks();
    fetchSettings();
  }, []);

  const handleMoveLeft = async (task) => {
    const newStatus = task.status === 'in-progress' ? 'todo' : 'in-progress';
    try {
      const response = await fetch(`${API_BASE_URL}/tasks/${task.id}/status`, {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ status: newStatus })
      });
      
      if (!response.ok) {
        const errorData = await response.json();
        alert(errorData.detail?.message || 'Failed to move task');
        return;
      }
      
      await fetchTasks();
    } catch (err) {
      alert('Error moving task: ' + err.message);
    }
  };

  const handleMoveRight = async (task) => {
    const newStatus = task.status === 'todo' ? 'in-progress' : 'done';
    try {
      const response = await fetch(`${API_BASE_URL}/tasks/${task.id}/status`, {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ status: newStatus })
      });
      
      if (!response.ok) {
        const errorData = await response.json();
        alert(errorData.detail?.message || 'Failed to move task');
        return;
      }
      
      await fetchTasks();
    } catch (err) {
      alert('Error moving task: ' + err.message);
    }
  };

  const handleEdit = (task) => {
    setSelectedTask(task);
    setEditModalOpen(true);
  };

  const handleSaveEdit = async (taskId, updates) => {
    try {
      const response = await fetch(`${API_BASE_URL}/tasks/${taskId}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(updates)
      });
      
      if (!response.ok) throw new Error('Failed to update task');
      await fetchTasks();
    } catch (err) {
      alert('Error updating task: ' + err.message);
    }
  };

  const handleDelete = (task) => {
    setSelectedTask(task);
    setDeleteModalOpen(true);
  };

  const handleConfirmDelete = async (taskId) => {
    try {
      const response = await fetch(`${API_BASE_URL}/tasks/${taskId}`, {
        method: 'DELETE'
      });
      
      if (!response.ok) throw new Error('Failed to delete task');
      await fetchTasks();
    } catch (err) {
      alert('Error deleting task: ' + err.message);
    }
  };

  const handleCreateTask = async (taskData) => {
    try {
      const response = await fetch(`${API_BASE_URL}/tasks/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(taskData)
      });
      
      if (!response.ok) throw new Error('Failed to create task');
      await fetchTasks();
    } catch (err) {
      alert('Error creating task: ' + err.message);
    }
  };

  const handleSaveSettings = async (newWipLimit) => {
    try {
      const response = await fetch(`${API_BASE_URL}/settings/`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ wip_limit: newWipLimit })
      });
      
      if (!response.ok) throw new Error('Failed to update settings');
      await fetchSettings();
    } catch (err) {
      alert('Error updating settings: ' + err.message);
    }
  };

  const backlogTasks = tasks.filter(t => t.status === 'todo');
  const inProgressTasks = tasks.filter(t => t.status === 'in-progress');
  const doneTasks = tasks.filter(t => t.status === 'done');

  if (loading) {
    return <div className="App"><div className="loading">Loading...</div></div>;
  }

  return (
    <div className="App">
      <header className="app-header">
        <h1>WIP Planner</h1>
        <button className="btn-settings" onClick={() => setSettingsModalOpen(true)}>Settings ▼</button>
      </header>

      {error && <div className="error-banner">Error: {error}</div>}

      <div className="board">
        <Column
          title="Backlog"
          tasks={backlogTasks}
          onMoveLeft={handleMoveLeft}
          onMoveRight={handleMoveRight}
          onEdit={handleEdit}
          onDelete={handleDelete}
        />
        <Column
          title="In Progress"
          tasks={inProgressTasks}
          wipLimit={wipLimit}
          onMoveLeft={handleMoveLeft}
          onMoveRight={handleMoveRight}
          onEdit={handleEdit}
          onDelete={handleDelete}
        />
        <Column
          title="Done"
          tasks={doneTasks}
          onMoveLeft={handleMoveLeft}
          onMoveRight={handleMoveRight}
          onEdit={handleEdit}
          onDelete={handleDelete}
        />
      </div>

      <button className="btn-new-task" onClick={() => setNewTaskModalOpen(true)}>
        <span className="plus-icon">+</span> New Task
      </button>

      <EditTaskModal
        task={selectedTask}
        isOpen={editModalOpen}
        onClose={() => setEditModalOpen(false)}
        onSave={handleSaveEdit}
        onDelete={handleDelete}
      />

      <DeleteTaskModal
        task={selectedTask}
        isOpen={deleteModalOpen}
        onClose={() => setDeleteModalOpen(false)}
        onConfirm={handleConfirmDelete}
      />

      <NewTaskModal
        isOpen={newTaskModalOpen}
        onClose={() => setNewTaskModalOpen(false)}
        onCreate={handleCreateTask}
      />

      <SettingsModal
        isOpen={settingsModalOpen}
        onClose={() => setSettingsModalOpen(false)}
        wipLimit={wipLimit}
        onSave={handleSaveSettings}
      />
    </div>
  );
}

export default App;
