export interface Sentence {
  text: string;
  duration: number; // in milliseconds
}

export type DisplayMode = 'sequential' | 'random';
export type Theme = 'dark' | 'light' | 'ocean' | 'forest' | 'sunset';

export interface AppState {
  inputText: string;
  sentences: Sentence[];
  currentIndex: number;
  isPlaying: boolean;
  isInputMode: boolean;
  displayMode: DisplayMode;
  randomOrder: number[]; // Indices of sentences in random order
  theme: Theme;
  fontWeight: number; // Font weight (100-900)
}

export type AppAction =
  | { type: 'SET_INPUT_TEXT'; payload: string }
  | { type: 'START_DISPLAY'; payload: Sentence[] }
  | { type: 'TOGGLE_PLAY' }
  | { type: 'NEXT_SENTENCE' }
  | { type: 'PREV_SENTENCE' }
  | { type: 'TOGGLE_MODE' }
  | { type: 'RESET_INPUT' }
  | { type: 'SET_THEME'; payload: Theme }
  | { type: 'SET_FONT_WEIGHT'; payload: number };
