export interface Feature {
  icon: string;
  title: string;
  description: string;
  colorClass: {
    bg: string;
    text: string;
  };
  isVisible?: boolean;
}
