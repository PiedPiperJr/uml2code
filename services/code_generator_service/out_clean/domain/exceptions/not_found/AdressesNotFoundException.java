package mwm.domain.exceptions.not_found;

import mwm.domain.exceptions.EntityNotFoundException;

public class AdressesNotFoundException extends EntityNotFoundException {
public AdressesNotFoundException(String message) {
        super(message);
    }
}