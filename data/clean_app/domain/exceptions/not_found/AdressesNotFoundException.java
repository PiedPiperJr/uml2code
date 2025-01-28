package org.enspy.4gi.domain.exceptions.not_found;

import org.enspy.4gi.domain.exceptions.EntityNotFoundException;

public class AdressesNotFoundException extends EntityNotFoundException {
public AdressesNotFoundException(String message) {
        super(message);
    }
}