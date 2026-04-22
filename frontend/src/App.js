import React, { useState } from 'react';
import './App.css';

// Sample hardcoded tasks for layout
const sampleTasks = [
  { id: '1', title: 'Task 1: Initial design', description: '', status: 'todo' },
  { id: '2', title: 'Task 2: Research Ideas', description: '', status: 'todo' },
  { id: '3', title: 'Task 3: Build Prototype', description: '', status: 'in-progress' },
  { id: '4', title: 'Task 4: Write Report', description: '', status: 'done' },
];

function TaskCard({ task, onMoveLeft, onMoveRight, onDelete }) {
  const canMoveLeft = task.status !== 'todo';
  const canMoveRight = task.status !== 'done';

  return (
    <div className="task-card">
      <div className="task-title">{task.title}</div>
      {task.description && <div className="task-description">{task.description}</div>}
      
      <div className="task-actions">
        {canMoveLeft && (
          <button className="btn-move" onClick={() => onMoveLeft(task.id)}>
            Move ←
          </button>
        )}
        {canMoveRight && (
          <button className="btn-move" onClick={() => onMoveRight(task.id)}>
            Move →
          </button>
        )}
        <button className="btn-delete" onClick={() => onDelete(task.id)}>
          Delete
        </button>
      </div>
    </div>
  );
}

function Column({ title, tasks, wipLimit, onMoveLeft, onMoveRight, onDelete }) {
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
              onDelete={onDelete}
            />
          ))
        )}
      </div>
    </div>
  );
}

function App() {
  const [tasks, setTasks] = useState(sampleTasks);
  const [wipLimit] = useState(1);

  const handleMoveLeft = (taskId) => {
    setTasks(tasks.map(task => {
      if (task.id === taskId) {
        const newStatus = task.status === 'in-progress' ? 'todo' : 'in-progress';
        return { ...task, status: newStatus };
      }
      return task;
    }));
  };

  const handleMoveRight = (taskId) => {
    setTasks(tasks.map(task => {
      if (task.id === taskId) {
        const newStatus = task.status === 'todo' ? 'in-progress' : 'done';
        return { ...task, status: newStatus };
      }
      return task;
    }));
  };

  const handleDelete = (taskId) => {
    setTasks(tasks.filter(task => task.id !== taskId));
  };

  const backlogTasks = tasks.filter(t => t.status === 'todo');
  const inProgressTasks = tasks.filter(t => t.status === 'in-progress');
  const doneTasks = tasks.filter(t => t.status === 'done');

  return (
    <div className="App">
      <header className="app-header">
        <h1>WIP Planner</h1>
        <button className="btn-settings">Settings ▼</button>
      </header>

      <div className="board">
        <Column
          title="Backlog"
          tasks={backlogTasks}
          onMoveLeft={handleMoveLeft}
          onMoveRight={handleMoveRight}
          onDelete={handleDelete}
        />
        <Column
          title="In Progress"
          tasks={inProgressTasks}
          wipLimit={wipLimit}
          onMoveLeft={handleMoveLeft}
          onMoveRight={handleMoveRight}
          onDelete={handleDelete}
        />
        <Column
          title="Done"
          tasks={doneTasks}
          onMoveLeft={handleMoveLeft}
          onMoveRight={handleMoveRight}
          onDelete={handleDelete}
        />
      </div>

      <button className="btn-new-task">
        <span className="plus-icon">+</span> New Task
      </button>
    </div>
  );
}

export default App;
