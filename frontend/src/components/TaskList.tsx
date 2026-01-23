import { useEffect, useState } from "react";
import { api, Task } from "../api";

export const TaskList = () => {
    const [tasks, setTasks] = useState<Task[]>([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        setLoading(true);
        api
        .getTasks()
        .then(setTasks)
        .catch((e) => setError(e.message))
        .finally(() => setLoading(false));
    }, []);

    return (
        <div className="card">
        <h2>Все задачи</h2>
        <p>Сырые данные из /tasks.</p>

        {loading && <p>Загрузка...</p>}
        {error && <p style={{ color: "#f97373" }}>Ошибка: {error}</p>}

        <ul className="list">
            {tasks.map((t) => (
            <li key={t.id} className="list-item">
                <span>{t.name}</span>
                <span className="badge">
                id: {t.id}
                {t.category_id != null && ` · cat: ${t.category_id}`}
                </span>
            </li>
            ))}
            {!loading && !error && tasks.length === 0 && (
            <p style={{ color: "#9ca3af", fontSize: 13 }}>Задач пока нет.</p>
            )}
        </ul>
        </div>
    );
};
