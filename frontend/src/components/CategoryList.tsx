import { useEffect, useState } from "react";
import { api, Category } from "../api";

interface Props {
    selectedId: number | null;
    onSelect: (id: number | null) => void;
    }

    export const CategoryList = ({ selectedId, onSelect }: Props) => {
    const [categories, setCategories] = useState<Category[]>([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        setLoading(true);
        api
        .getCategories()
        .then(setCategories)
        .catch((e) => setError(e.message))
        .finally(() => setLoading(false));
    }, []);

    return (
        <div className="card">
        <h2>Категории</h2>
        <p>Выбери категорию, чтобы увидеть задачи.</p>

        {loading && <p>Загрузка...</p>}
        {error && <p style={{ color: "#f97373" }}>Ошибка: {error}</p>}

        <ul className="list">
            {categories.map((c) => (
            <li
                key={c.id}
                className="list-item"
                style={{
                borderColor: selectedId === c.id ? "#4f46e5" : "#1f2937",
                boxShadow:
                    selectedId === c.id
                    ? "0 0 0 1px rgba(79,70,229,0.4)"
                    : "none"
                }}
                onClick={() => onSelect(selectedId === c.id ? null : c.id)}
            >
                <span>{c.name}</span>
                <span className="badge">id: {c.id}</span>
            </li>
            ))}
            {!loading && !error && categories.length === 0 && (
            <p style={{ color: "#9ca3af", fontSize: 13 }}>Категорий пока нет.</p>
            )}
        </ul>
        </div>
    );
};
