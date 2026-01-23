import { useEffect, useState } from "react";
import { api, Task } from "../api";

interface Props {
    categoryId: number | null;
    }

    export const TasksByCategory = ({ categoryId }: Props) => {
    const [tasks, setTasks] = useState<Task[]>([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        if (categoryId == null) {
        setTasks([]);
        setError(null);
        return;
        }
        setLoading(true);
        api
        .getTasksByCategory(categoryId)
        .then(setTasks)
        .catch((e) => setError(e.message))
        .finally(() => setLoading(false));
    }, [categoryId]);

    return (
        <div className="card">
        <h2>Задачи по категории</h2>
        <p>
            {categoryId == null
            ? "Выбери категорию слева."
            : `Категория id: ${categoryId}`}
        </p>

        {loading && <p>Загрузка...</p>}
        {error && <p style={{ color: "#f97373" }}>Ошибка: {error}</p>}

        <ul className="list">
            {tasks.map((t) => (
            <li key={t.id} className="list-item">
                <span>{t.name}</span>
                <span className="badge">id: {t.id}</span>
            </li>
            ))}
            {!loading && !error && categoryId != null && tasks.length === 0 && (
            <p style={{ color: "#9ca3af", fontSize: 13 }}>
                В этой категории задач нет.
            </p>
            )}
        </ul>
        </div>
    );
};
