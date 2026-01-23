import { ReactNode } from "react";

export const Layout = ({ children }: { children: ReactNode }) => {
    return (
        <div className="app-root">
        <header>
            <div>
            <h1>DisciplineApp</h1>
            <span>Мини-панель для твоего FastAPI backend</span>
            </div>
            <span>frontend · React + TS</span>
        </header>
        {children}
        <footer>© DisciplineApp · сделано тобой и чуть-чуть мной</footer>
        </div>
    );
};
