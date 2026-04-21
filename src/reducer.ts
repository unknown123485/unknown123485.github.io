import { AppState, AppAction } from './types';
import { shuffleArray } from './utils';

export const initialState: AppState = {
  inputText: '',
  sentences: [],
  currentIndex: 0,
  isPlaying: false,
  isInputMode: true,
  displayMode: 'random', // Default to random mode as requested
  randomOrder: [],
  theme: 'dark', // Default to dark theme
  fontWeight: 400, // Default font weight
};

export function reducer(state: AppState, action: AppAction): AppState {
  switch (action.type) {
    case 'SET_INPUT_TEXT':
      return { ...state, inputText: action.payload };
    
    case 'START_DISPLAY': {
      const sentences = action.payload;
      const indices = Array.from({ length: sentences.length }, (_, i) => i);
      const randomOrder = shuffleArray(indices);
      return {
        ...state,
        sentences,
        isInputMode: false,
        isPlaying: true,
        currentIndex: 0,
        randomOrder,
      };
    }

    case 'TOGGLE_PLAY':
      return { ...state, isPlaying: !state.isPlaying };

    case 'NEXT_SENTENCE': {
      const nextIndex = (state.currentIndex + 1) % state.sentences.length;
      return { ...state, currentIndex: nextIndex };
    }

    case 'PREV_SENTENCE': {
      const prevIndex = (state.currentIndex - 1 + state.sentences.length) % state.sentences.length;
      return { ...state, currentIndex: prevIndex };
    }

    case 'TOGGLE_MODE': {
      const newMode = state.displayMode === 'random' ? 'sequential' : 'random';
      return { ...state, displayMode: newMode };
    }

    case 'RESET_INPUT':
      return { ...initialState, inputText: state.inputText, theme: state.theme, fontWeight: state.fontWeight };

    case 'SET_THEME':
      return { ...state, theme: action.payload };

    case 'SET_FONT_WEIGHT':
      return { ...state, fontWeight: action.payload };

    default:
      return state;
  }
}
