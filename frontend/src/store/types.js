const cardTypes = {
  SET_MESSAGE: "SET_MESSAGE",
  SET_TEXT_ISVISIBLE: "SET_TEXT_ISVISIBLE",
  SET_MENU_STICKER_ISVISIBLE: "SET_MENU_STICKER_ISVISIBLE",
  SET_MENU_BACKGROUND_ISVISIBLE: "SET_MENU_BACKGROUND_ISVISIBLE",
  SET_MENU_TEXT_ISVISIBLE: "SET_MENU_TEXT_ISVISIBLE",

  SET_BACKGROUND_COLOR: "SET_BACKGROUND_COLOR",
  SET_BACKGROUND_IMAGE: "SET_BACKGROUND_IMAGE",
  REMOVE_BACKGROUND: "REMOVE_BACKGROUND",

  ADD_STICKER: "ADD_STICKER",
  REMOVE_STICKER: "REMOVE_STICKER",
  SET_STICKER_POS: "SET_STICKER_POS",
  SET_STICKER_SCALE: "SET_STICKER_SCALE",

  SET_CARD_ID: "SET_CARD_ID",
  RESET_CARD: "RESET_CARD",
};

const types = {
  ...cardTypes,
};

export default types;
