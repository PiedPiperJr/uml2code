package mwm.domain.exceptions.not_found;

import mwm.domain.exceptions.EntityNotFoundException;

public class AddressNotFoundException extends EntityNotFoundException {
public AddressNotFoundException(String message) {
        super(message);
    }
}