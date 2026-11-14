interface PlaceholderPageProps {
  title: string;
  description: string;
  icon: string;
}

export function PlaceholderPage({ title, description, icon }: PlaceholderPageProps) {
  return (
    <div className="flex flex-col items-center justify-center py-20 text-center">
      <div className="text-6xl mb-6">{icon}</div>
      <h1 className="text-2xl font-bold text-white mb-3">{title}</h1>
      <p className="text-gray-400 max-w-md">{description}</p>
      <p className="text-gray-600 text-sm mt-4">Coming in a future milestone</p>
    </div>
  );
}
