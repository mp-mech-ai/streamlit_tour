// Tells tsc that importing any .css file is valid (Vite handles it at runtime)
declare module "*.css" {
  const content: Record<string, string>;
  export default content;
}