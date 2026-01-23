import "./styles.css";
import { Layout } from "./components/Layout";
import { CategoryList } from "./components/CategoryList";
import { TaskList } from "./components/TaskList";
import { TasksByCategory } from "./components/TasksByCategory";
import { useState } from "react";

export const App = () => {
  const [selectedCategoryId, setSelectedCategoryId] = useState<number | null>(
    null
  );

  return (
    <Layout>
      <main>
        <div>
          <CategoryList
            selectedId={selectedCategoryId}
            onSelect={setSelectedCategoryId}
          />
        </div>
        <div>
          <TaskList />
          <div style={{ marginTop: 16 }}>
            <TasksByCategory categoryId={selectedCategoryId} />
          </div>
        </div>
      </main>
    </Layout>
  );
};
